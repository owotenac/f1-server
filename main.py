from races import getRaces
from store import storeRaces, storeSessionsResults
from sessions import getSessions 
from session_result import get_session_result
from drivers_standing import drivers_standing
from constructors_standing import constructors_standing   
from briefing import generate_briefing, get_briefing

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "DELETE"],
    allow_headers=["Content-Type"],
)

@app.get("/")
def index():
    return "Ready"

app.add_api_route('/api/v1/meetings', getRaces, methods=["GET"])
app.add_api_route('/api/v1/sessions', getSessions, methods=["GET"])
app.add_api_route('/api/v1/session_result', get_session_result,  methods=["GET"])
app.add_api_route('/api/v1/drivers_standing', drivers_standing,  methods=["GET"])
app.add_api_route('/api/v1/constructors_standing', constructors_standing,  methods=["GET"])

app.add_api_route('/api/v1/storeRaces', storeRaces, methods=["POST"])
app.add_api_route('/api/v1/storeSessionsResults', storeSessionsResults, methods=["POST"])

app.add_api_route('/api/v1/generate-briefing', generate_briefing, methods=["POST"])
app.add_api_route('/api/v1/briefing', get_briefing, methods=["GET"])


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

# if __name__ == "__main__":
#     main()