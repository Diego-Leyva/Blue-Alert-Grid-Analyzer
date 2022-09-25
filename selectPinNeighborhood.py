import os
import time
import math
import random
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv(find_dotenv())

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

@app.route("/getPins", methods=['GET', 'POST'])
@cross_origin()
def calculatePins():
    try:
        pins = []
        client = MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{IP}:{PORT}/")

        db = client["coordinates"]
    
        db = db["grids"]

        for x in db.find():
            if(x['stateCode'] == request.args.get("state")):
                random.seed(int(math.sqrt(time.time())**2))
                n = random.choice(range(0, 24))
                pins.append(x['points'][n])
            else:
                pins.append([-1, -1])
            
        return {
            "pins": pins
        }
    
    except:
        return {
            "error": "Bad Query"
        }

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port="9999")