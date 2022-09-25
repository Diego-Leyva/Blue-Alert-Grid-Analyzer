import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import math

load_dotenv(find_dotenv())

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

def get_database():

    client = MongoClient(f"mongodb://{USERNAME}:{PASSWORD}@{IP}:{PORT}/")

    db = client["coordinates"]
 
    col = db["grids"]
    
    return col


def calculateNeighborhoodSize(db):
    for data in db.find():
        bottom = math.sqrt((float(data['LatRightBot']) - float(data['LatLeftBot']))**2 + (float(data['LongRightBot']) - float(data['LongLeftBot']))**2)
        left = math.sqrt((float(data['LatLeftBot']) - float(data['LatLeftUp']))**2 + (float(data['LongLeftBot']) - float(data['LongLeftUp']))**2)
        right = math.sqrt((float(data['LatRightBot']) - float(data['LatRightUp']))**2 + (float(data['LongRightBot']) - float(data['LongRightUp']))**2)
        up = math.sqrt((float(data['LatLeftUp']) - float(data['LatRightUp']))**2 + (float(data['LongLeftUp']) - float(data['LongRightUp']))**2)
        points = []

        if(bottom*left >= right*up): 
            area = right*up
        
            for x in range(5):
                pointLat = float(data['LatRightBot'])+(x*right/5)
                for i in range(5):
                    pointLong = float(data['LongRightBot'])+(i*right/5)

                    points.append([pointLat, pointLong])

        else:
            area=bottom*left

        db.update_one(data, {"$set": {"bottom": str(bottom), "left": str(left), "right": str(right), "up": str(up), "area": str(area), "points": points}})

calculateNeighborhoodSize(get_database())