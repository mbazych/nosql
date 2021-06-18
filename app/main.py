from flask import Flask, render_template, request, make_response, jsonify
from geopy.geocoders import Nominatim
from flask_pymongo import PyMongo
import json
import os

application = Flask(__name__)

application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
    '@' + os.environ['MONGODB_HOSTNAME'] + \
    ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(application)
conn = mongo.db


@application.route("/")
def index():
    return render_template("templates/index.html")


@application.route("/api/v1.0/tasks/autoc2/restaurantfinder", methods=["GET"])
def getrestaurants():
    restname = request.args.get("restaurant")
    city = request.args.get("city")
    state = request.args.get("state")
    zipcode = request.args.get("zipcode")
    rad = request.args.get("radius")
    print(rad)
    print(type(rad))

    print(restname, city, state, zipcode)

    zip_or_addr = city + " " + state + " " + zipcode
    print(zip_or_addr)
    print(f"zip_or_addr: {zip_or_addr}")

    geolocator = Nominatim(user_agent="myapplicationlication")
    location = geolocator.geocode(zip_or_addr, timeout=10000)
    lat = float(location.raw["lat"])
    lon = float(location.raw["lon"])
    nearby_restaurants = [{"orig_lat": lat, "orig_lon": lon}]

    print(lat, lon)


# {"_id":{"$oid":"55cba2476c522cafdb056c36"},"location":{"coordinates":[-73.9160315,40.7629446],"type":"Point"},"name":"Kentucky Fried Chicken"}

    METERS_PER_MILE = 1609.34

    filters = {"location": {"$nearSphere": {"$geometry": {"type": "Point",
                                                          "coordinates": [float(lon), float(lat)]},
                                            "$maxDistance": int(rad) * METERS_PER_MILE}},
               "name": {"$regex": restname, "$options": "i"}}

    cursor = conn.find(filters)

    for cur in cursor:
        nearby_restaurants.applicationend({
            "restaurant_name": cur["name"],
            "lat": cur["location"]["coordinates"][1],
            "lon": cur["location"]["coordinates"][0]
        })
    print("Restaurants: ")
    print(json.dumps(nearby_restaurants))
    return jsonify(nearby_restaurants)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
