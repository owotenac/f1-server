from races import getRaces
from sessions import getSessions 
from session_result import get_session_result
from flask_cors import CORS
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return "Ready"

app.add_url_rule('/v1/meetings', 'getRaces', getRaces)
app.add_url_rule('/v1/sessions', 'getSessions', getSessions)
app.add_url_rule('/v1/session_result', 'get_session_result', get_session_result)


CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def main():
    app.run(debug=True,port=5001 , use_reloader=False)