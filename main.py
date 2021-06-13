from flask import Flask, request, jsonify
from flask_cors import CORS
import rentList as rl

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "This is the Api for 591."

@app.route('/rentList', methods=['POST'])
def findRent():
    try:
        result = rl.dealJson(request.get_json())
        
    except Exception as e:
        result = {
            "status": "error",
            "message": repr(e),
        }

    return jsonify(result)
    

if __name__ == "__main__":
    #turn false on server
    app.run(host="0.0.0.0", port="5000", debug=True)