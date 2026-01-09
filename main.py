from races import getRaces
from sessions import getSessions 
from session_result import get_session_result
from drivers_standing import drivers_standing
from constructors_standing import constructors_standing   
from flask_cors import CORS
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return "Ready"

app.add_url_rule('/v1/meetings', 'getRaces', getRaces)
app.add_url_rule('/v1/sessions', 'getSessions', getSessions)
app.add_url_rule('/v1/session_result', 'get_session_result', get_session_result)
app.add_url_rule('/v1/drivers_standing', 'drivers_standing', drivers_standing)
app.add_url_rule('/v1/constructors_standing', 'constructors_standing', constructors_standing)





CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def main():
    app.run(debug=True,port=5001 , use_reloader=False)