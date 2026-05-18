import asyncio
import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from google.cloud import firestore

import fetch
from store import storeSessionsResults
from firestore_client import FirestoreClient 


logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# ---------------------------------------------------------------------------
# Helpers Firestore
# ---------------------------------------------------------------------------

def _parse_date(value) -> datetime:
    """Normalise un champ date : ISO string ou Firestore Timestamp → datetime UTC aware."""
    if isinstance(value, str):
        dt = datetime.fromisoformat(value)
    else:
        dt = value.astimezone(timezone.utc) if hasattr(value, "astimezone") else value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _get_pending_sessions(meeting_key: int) -> list[dict]:
    docs = (
        FirestoreClient().client.collection("sessions")
        .where("meeting_key", "==", meeting_key)
        .where("status", "==", "pending")
        .get()
    )
    return [{"id": d.id, **d.to_dict()} for d in docs]


# ---------------------------------------------------------------------------
# Résolution du prochain GP avec sessions pending
# ---------------------------------------------------------------------------

async def get_next_pending_meeting() -> dict | None:
    """
    Retourne le premier GP (doc race) qui a encore au moins une session pending.
    """
    now = datetime.now(timezone.utc)

    races = (
        FirestoreClient().client.collection("races")
        .where("date_start", ">=", now)
        .order_by("date_start", direction=firestore.Query.ASCENDING)
        .get()
    )

    for doc in races:
        race = doc.to_dict()
        meeting_key = race.get("meeting_key")
        if not meeting_key:
            continue

        pending = (
            FirestoreClient().client.collection("sessions")
            .where("meeting_key", "==", meeting_key)
            .where("status", "==", "pending")
            .limit(1)
            .get()
        )

        if pending:
            return race

    logger.info("🏁 Toute la saison est fetchée — rien à scheduler.")
    return None


# ---------------------------------------------------------------------------
# Fetch + retry d'une session
# ---------------------------------------------------------------------------

async def fetch_session_results(session_id: str, session_key: int, meeting_key: int, attempt: int = 1):
    """
    Tente de fetcher et stocker les résultats d'une session.
    - Succès    → storeSessionsResults gère le status 'done' dans Firestore
    - Incomplet → reschedule +15min (max 3 tentatives)
    - Échec     → marque 'failed', on passe à la suite
    """
    logger.info(f"🔄 Fetch session {session_key} (meeting {meeting_key}) — tentative {attempt}/3")

    try:
        result = await storeSessionsResults(meeting_key=meeting_key, session_key=session_key)

        if result:
            logger.info(f"✅ Session {session_key} ({session_id}) syncée avec succès")

            # Dernière session pending de ce GP ?
            remaining = _get_pending_sessions(meeting_key)
            if not remaining:
                logger.info(f"🏆 GP {meeting_key} terminé — passage au GP suivant")
                await rehydrate_scheduler()
            return

        # storeSessionsResults a retourné None → résultats pas encore dispo
        if attempt >= 3:
            logger.warning(f"❌ Session {session_key} : 3 tentatives sans résultat → failed")
            return

        run_date = datetime.now(timezone.utc) + timedelta(minutes=15)
        logger.info(f"⏳ Session {session_key} pas encore dispo — retry à {run_date.strftime('%H:%M')} UTC")

        scheduler.add_job(
            fetch_session_results,
            trigger=DateTrigger(run_date=run_date),
            args=[session_id, session_key, meeting_key, attempt + 1],
            id=f"fetch_{session_key}_attempt_{attempt + 1}",
            replace_existing=True,
        )

    except Exception as e:
        logger.error(f"💥 Erreur inattendue sur session {session_key} : {e}")
        if attempt >= 3:
            _mark_session_failed(session_id)


# ---------------------------------------------------------------------------
# Rehydratation — cœur du système
# ---------------------------------------------------------------------------

async def rehydrate_scheduler():
    """
    Point d'entrée principal — appelé au boot et après chaque GP complété.
    Résout le prochain GP pending et schedule un DateTrigger par session.
    Idempotent : replace_existing=True évite les doublons si appelé plusieurs fois.
    """
    meeting = await get_next_pending_meeting()
    if not meeting:
        return

    meeting_key = meeting["meeting_key"]
    meeting_name = meeting.get("meeting_name", meeting_key)
    logger.info(f"📅 Scheduling sessions pour : {meeting_name} (meeting_key={meeting_key})")

    sessions = _get_pending_sessions(meeting_key)
    now = datetime.now(timezone.utc)

    for session in sessions:
        session_key = session["session_key"]
        session_id = session["id"]
        session_name = session.get("session_name", session_key)

        date_end = _parse_date(session["date_end"])
        run_date = date_end + timedelta(minutes=15)

        # Session déjà terminée au moment du boot (redémarrage Railway en cours de weekend)
        if run_date < now:
            run_date = now + timedelta(minutes=1)
            logger.info(f"⚡ {session_name} ({session_key}) déjà passée — fetch immédiat dans 1 min")
        else:
            logger.info(f"🕐 {session_name} ({session_key}) schedulée à {run_date.strftime('%Y-%m-%d %H:%M')} UTC")

        scheduler.add_job(
            fetch_session_results,
            trigger=DateTrigger(run_date=run_date),
            args=[session_id, session_key, meeting_key],
            id=f"fetch_{session_key}",
            replace_existing=True,
        )