"""
F1 Briefing Generator
---------------------
Génère un briefing pré-GP via Ollama et le stocke dans Firestore.
Déclenchement : POST /api/v1/generate-briefing?year=2025&round=6

Sources :
  - Jolpica  : résultats dernières courses, standings, infos circuit
  - Open-Meteo : météo forecast du weekend
  - Ollama   : narration LLM locale
  - Firestore : stockage du briefing généré
"""

import asyncio
import json
import requests
from datetime import datetime
from fastapi import HTTPException
import firebase_admin
from firebase_admin import firestore
import fetch
from config import JOLPICA_BASE_URL, OPEN_METEO_BASE_URL
import traceback

OLLAMA_URL   = "http://localhost:11434/api/generate" 
OLLAMA_MODEL = "qwen2.5"


# ─── Collecte des données ─────────────────────────────────────────────────────

async def _get_next_gp(year: int, round: int) -> dict:
    """Infos du prochain GP"""
    data  = await fetch.api_call(f"{JOLPICA_BASE_URL}/{year}/{round}.json")
    race  = data["MRData"]["RaceTable"]["Races"][0]
    circ  = race["Circuit"]
    loc   = circ["Location"]

    return {
        "name":         race["raceName"],
        "round":        int(race["round"]),
        "season":       int(race["season"]),
        "date":         race["date"],
        "circuit_id":   circ["circuitId"],
        "circuit_name": circ["circuitName"],
        "location":     loc["locality"],
        "country":      loc["country"],
        "lat":          float(loc["lat"]),
        "lng":          float(loc["long"]),
    }


async def _get_last_results(year: int, last_n: int = 3) -> list:
    """Résultats des N dernières courses pour la forme des pilotes"""
    # Récupère le calendrier pour trouver les derniers rounds disputés
    data  = await fetch.api_call(f"{JOLPICA_BASE_URL}/{year}/results.json")
    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", []) or []

    if last_n <= 0 or not races:
        return []

    # On prend au maximum les courses disponibles sans lever d'erreur
    start_index = max(len(races) - last_n, 0)
    selected_races = races[start_index:]

    results = []
    for race in selected_races:
        top5 = []
        for r in race.get("Results", [])[:5]:
            top5.append({
                "position": int(r["position"]),
                "driver":   r["Driver"]["code"],
                "team":     r["Constructor"]["name"],
                #"from_grid": int(r.get("grid", 0)),
                "status":   r.get("status"),
            })
        results.append({
            "race":  race["raceName"],
            "round": int(race["round"]),
            "top5":  top5,
        })

    return results


async def _get_circuit_history(circuit_id: str, year: int, last_n: int = 5) -> dict:
    """Historique des vainqueurs sur ce circuit"""
    winners       = []
    pole_to_win   = 0

    for y in range(year - 1, year - last_n - 1, -1):
        data  = await fetch.api_call(
            f"{JOLPICA_BASE_URL}/{y}/circuits/{circuit_id}/results/1.json"
        )
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not races:
            continue

        r    = races[0]["Results"][0]
        grid = int(r.get("grid", 0))
        if grid == 1:
            pole_to_win += 1

        winners.append({
            "year":      y,
            "driver":    f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
            "drive_code": r["Driver"]["code"],
            "team":      r["Constructor"]["name"],
            "from_grid": grid,
        })

    return {
        "last_winners":     winners,
        "pole_to_win_rate": round(pole_to_win / len(winners), 2) if winners else 0,
    }


async def _get_standings(year: int) -> dict:
    """Standings pilotes et constructeurs — retourne vide si pas encore de course"""
    drivers_data, constructors_data = await asyncio.gather(
        fetch.api_call(f"{JOLPICA_BASE_URL}/{year}/driverstandings.json"),
        fetch.api_call(f"{JOLPICA_BASE_URL}/{year}/constructorstandings.json"),
    )

    driver_lists      = drivers_data["MRData"]["StandingsTable"].get("StandingsLists", [])
    constructor_lists = constructors_data["MRData"]["StandingsTable"].get("StandingsLists", [])

    if not driver_lists or not constructor_lists:
        return {"drivers": [], "constructors": []}

    drivers = [
        {
            "position": int(d["position"]),
            "driver":   d["Driver"]["code"],
            "team":     d["Constructors"][0]["name"],
            "points":   float(d["points"]),
            "wins":     int(d["wins"]),
        }
        for d in driver_lists[0].get("DriverStandings", [])[:10]
    ]

    constructors = [
        {
            "position": int(c["position"]),
            "team":     c["Constructor"]["name"],
            "points":   float(c["points"]),
            "wins":     int(c["wins"]),
        }
        for c in constructor_lists[0].get("ConstructorStandings", [])[:6]
    ]

    return {"drivers": drivers, "constructors": constructors}


async def _get_weather_forecast(lat: float, lng: float, race_date: str) -> list:
    """Météo forecast Open-Meteo pour le weekend"""
    data = await fetch.api_call(
        OPEN_METEO_BASE_URL,
        params={
            "latitude":      lat,
            "longitude":     lng,
            "daily":         "temperature_2m_max,precipitation_probability_max,windspeed_10m_max",
            "forecast_days": 7,
            "timezone":      "auto",
        }
    )

    daily  = data.get("daily", {})
    dates  = daily.get("time", [])
    temps  = daily.get("temperature_2m_max", [])
    rains  = daily.get("precipitation_probability_max", [])
    winds  = daily.get("windspeed_10m_max", [])

    # Filtre sur les 3 jours du weekend (vendredi → dimanche)
    forecast = []
    for i, date in enumerate(dates):
        if date >= race_date[:8] + "01":  # approximation — garde les jours pertinents
            forecast.append({
                "date":             date,
                "temp_max_celsius": temps[i] if i < len(temps) else None,
                "rain_probability": round((rains[i] or 0) / 100, 2) if i < len(rains) else None,
                "wind_kmh":         winds[i] if i < len(winds) else None,
            })

    return forecast[:4]  # vendredi → dimanche

async def _get_drivers_lineup(year: int) -> list:
    """Liste des pilotes et écuries engagés cette saison — toujours à jour"""
    data    = await fetch.api_call(f"{JOLPICA_BASE_URL}/{year}/drivers.json")
    drivers = data["MRData"]["DriverTable"].get("Drivers", [])

    # Pour avoir l'écurie on a besoin des standings ou du dernier round
    # On utilise driverstandings si dispo, sinon on retourne juste les pilotes
    standings_data = await fetch.api_call(
        f"{JOLPICA_BASE_URL}/{year}/driverstandings.json"
    )
    standings_lists = standings_data["MRData"]["StandingsTable"].get("StandingsLists", [])

    if standings_lists:
        # On a des standings — on récupère les associations pilote/écurie
        return [
            {
                "code":   d["Driver"]["code"],
                "name":   f"{d['Driver']['givenName']} {d['Driver']['familyName']}",
                "number": d["Driver"]["permanentNumber"],
                "team":   d["Constructors"][0]["name"],
            }
            for d in standings_lists[0].get("DriverStandings", [])
        ]
    else:
        # Début de saison — pas encore de standings, on retourne juste les pilotes sans écurie
        return [
            {
                "code":   d.get("code"),
                "name":   f"{d['givenName']} {d['familyName']}",
                "number": d.get("permanentNumber"),
                "team":   None,  # pas encore dispo
            }
            for d in drivers
        ]
    
# ─── Assemblage JSON ──────────────────────────────────────────────────────────

async def _build_briefing_data(year: int, round: int) -> dict:
    """Collecte toutes les données et assemble le JSON pour le LLM"""

    gp = await _get_next_gp(year, round)

    # Appels parallèles
    last_results, circuit_history, standings, weather, drivers_lineup = await asyncio.gather(
        _get_last_results(year),
        _get_circuit_history(gp["circuit_id"], year),
        _get_standings(year),
        _get_weather_forecast(gp["lat"], gp["lng"], gp["date"]),
        _get_drivers_lineup(year),        
    )

    return {
        "grand_prix":       gp,
        "circuit_history":  circuit_history,
        "last_races":       last_results,
        "standings":        standings,
        "weather_forecast": weather,
        "drivers_lineup":   drivers_lineup,        
    }


def _generate_narrative(data: dict) -> str:

    """Génère la narration via Ollama"""

    prompt = f"""
Tu es un ingénieur de piste F1 senior spécialisé en stratégie et dynamique véhicule. Génère un briefing technique pré-GP basé sur les données fournies. 

CONSIGNES STRICTES :
1. TON : Analytique, technique et factuel. Pas de jargon marketing.
2. RÉGLEMENTATION 2026 : Intègre les enjeux de la gestion d'énergie et de l'aéro active (X-Mode/Z-Mode) si c'est pertinent pour le tracé.
3. LIMITATIONS : Identifie les contraintes majeures liées au circuit (ex: usure pneus, importance de la traction, gestion de l'aero) et leur impact sur la stratégie.
4. COHÉRENCE : Utilise exclusivement les noms et codes pilotes fournis dans le 'drivers_lineup' et les 'standings'.

Réponds UNIQUEMENT en JSON avec cette structure exacte, sans markdown, sans texte avant ou après :
{{
  "headline": "Analyse de la hiérarchie technique pour ce GP",
  "circuit": "2-3 phrases sur le circuit et ses caractéristiques clés",
  "prediction": {{
    "top5": [
      {{"position": 1, "driver": "CODE", "team": "Team", "reason": "justification technique ou basée sur la forme récente"}},
      {{"position": 2, "driver": "CODE", "team": "Team", "reason": "justification technique ou basée sur la forme récente"}},
      {{"position": 3, "driver": "CODE", "team": "Team", "reason": "justification technique ou basée sur la forme récente"}},
      {{"position": 4, "driver": "CODE", "team": "Team", "reason": "justification technique ou basée sur la forme récente"}},
      {{"position": 5, "driver": "CODE", "team": "Team", "reason": "justification technique ou basée sur la forme récente"}}
    ]
  }},
  "key_point": "Le point tactique ou stratégique clé du weekend en 1 phrase, basé sur les données",
  "fun_stat": "Une stat surprenante ou anecdote historique sur ce circuit, basé sur les données",
    "technical_key_point": "Le défi d'ingénierie majeur du weekend (ex: compromis de setup ou pneu limiteur) en 1 phrase",
  "data_insight": "Une statistique historique ou une corrélation pole/victoire basée sur les données",
  "strategic_wildcard": "Le facteur imprévisible (météo, vent, Safety Car) et son impact technique précis"  
}}

Utilise les données suivantes pour construire ta narration :
{json.dumps(data, ensure_ascii=False, indent=2)}
LE JSON DOIT ÊTRE VALIDE.
La narration doit etre en FRANÇAIS."""

    #print(f"Generating narrative with data:\n{prompt}") 
    print(f"Data used:\n{json.dumps(data, ensure_ascii=False, indent=2)}")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model":  OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 800,
            }
        },
        timeout=120,
    )

    response.raise_for_status()
    raw = response.json()["response"].strip()

    # Nettoyage au cas où le LLM ajoute du markdown
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()

    print(f"LLM raw response:\n{raw}")

    return json.loads(raw)


# ─── Stockage Firestore ───────────────────────────────────────────────────────

def _store_briefing(year: int, round: int, briefing: dict) -> None:
    """Stocke le briefing dans Firestore"""
    db = firestore.client()
    db.collection("f1_briefings") \
      .document(f"{year}_{round}") \
      .set(briefing)


def _get_briefing_from_firestore(year: int, round: int) -> dict | None:
    """Récupère un briefing existant depuis Firestore"""
    db  = firestore.client()
    doc = db.collection("f1_briefings").document(f"{year}_{round}").get()
    return doc.to_dict() if doc.exists else None


# ─── Endpoints ────────────────────────────────────────────────────────────────

async def generate_briefing(year: int, round: int, force: bool = False):
    """
    POST /api/v1/generate-briefing?year=2025&round=6
    
    force=true pour régénérer même si déjà en cache
    """
    try:
        # Vérifie si déjà généré
        # if not force:
        #     existing = _get_briefing_from_firestore(year, round)
        #     if existing:
        #         return {"status": "cached", "briefing": existing}

        # Collecte des données
        data = await _build_briefing_data(year, round)

        # Génération LLM
        narrative = _generate_narrative(data)

        # Assemblage final
        briefing = {
            "generated_at": datetime.now().isoformat(),
            "year":         year,
            "round":        round,
            "grand_prix":   data["grand_prix"],
            #"data":         data,
            "narrative":    narrative,
        }

        print(f"Generated briefing for {year} R{round}:\n{json.dumps(briefing, ensure_ascii=False, indent=2)}")

        # Stockage Firestore
        #_store_briefing(year, round, briefing)

        return {"status": "generated", "briefing": briefing}

    except Exception as e:
        stack_str = traceback.format_exc() # string with full stack trace
        print(stack_str)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate briefing: {str(e)}"
        )


def get_briefing(year: int, round: int):
    """
    GET /api/v1/briefing?year=2025&round=6
    
    Retourne le briefing depuis Firestore s'il existe.
    """
    try:
        briefing = _get_briefing_from_firestore(year, round)

        if not briefing:
            return {"available": False, "message": "Briefing pas encore généré pour ce GP"}

        return {"available": True, "briefing": briefing}

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to get briefing: {str(e)}"
        )