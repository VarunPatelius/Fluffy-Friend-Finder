from flask import Flask, request, render_template, redirect, url_for, session
from petpy import Petfinder
from pprint import PrettyPrinter
from animal import Animal
import requests
import io
import folium
from time import sleep
from datetime import datetime as dt


ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXX"
SECRET = "XXXXXXXXXXXXXXXXXX"


app = Flask(__name__)
app.config["SECRET_KEY"] = "\]'/.;[pl,mkoijnbhuygvcftrdxzsewaq"


# Queries:
#  - animal_type - Dog/Cat/Rabbit
#  - breed - pf.breeds()
#  - size - ‘small’, ‘medium’, ‘large’, or ‘xlarge’
#  - gender - ‘male’, ‘female’, or ‘unknown’
#  - age - ‘baby’, ’young’, ‘adult’, ‘senior’
#  - color - pf.animal_types()["type"]["colors"]
#  - coat - ‘short’, ‘medium’, ‘long’, ‘wire’, ‘hairless’, or ‘curly’
#  - status - 'adoptable'
#  - location - 'lat, long'
#  - distance - <500, miles
#  - sort - 'distance'
#  - good_with_cats, good_with_children, good_with_dogs - True/False
#  - results_per_page - 10
#  - pages - 10


def get_pets(
        animal_type=None, 
        breed=None, 
        size=None, 
        gender=None, 
        age=None, 
        color=None, 
        coat=None, 
        lat=None, 
        long=None, 
        distance=None, 
        gwca=None, 
        gwch=None, 
        gwd=None
    ):
    pf = Petfinder(key=ACCESS_TOKEN, secret=SECRET)

    animals_data = pf.animals(
        animal_type=animal_type,
        breed=breed,
        size=size,
        gender=gender,
        age=age,
        color=color,
        coat=coat,
        status="adoptable",
        location=f"{lat}, {long}",
        distance=distance,
        sort="distance",
        good_with_cats=gwca,
        good_with_children=gwch,
        good_with_dogs=gwd,
        results_per_page=10,
        pages=10
    )["animals"]

    animals_list = []

    for animal in animals_data:
        animals_list.append(
            Animal(animal)
        )
    
    return animals_list


def store_map():
    latitude = session["lat"]
    longitude = session["lng"]
    COORDS = (latitude, longitude)
    storeMap = folium.Map(tiles='Stamen Terrain', zoom_start=12, location=COORDS, max_zoom=16, min_zoom=10)

    params = {
        "model.latitude": str(latitude),
        "model.longitude": str(longitude)
    }
    BASE_URL = "https://api.petsmart.com/stores/search"

    response = requests.get(BASE_URL, params=params)

    folium.Marker(COORDS, tooltip="Your Location", icon=folium.Icon(color="pink")).add_to(storeMap)

    for store in response.json()["StoreSearchResults"]:
        storeCharacteristics = store["Store"]
        storeName = storeCharacteristics["Name"]
        storeLat = storeCharacteristics["Latitude"]
        storeLon = storeCharacteristics["Longitude"]
        storeStreet = storeCharacteristics["StreetLine1"]
        storeServices = " • " + "<br> • ".join([service["ServiceName"] for service in storeCharacteristics["StoreServices"]])
        storeOpen = dt.strptime(storeCharacteristics["CurrentStoreHours"][0]["OpenTime"][:5], "%H:%M").strftime("%I:%M %p")
        storeClose = dt.strptime(storeCharacteristics["CurrentStoreHours"][0]["CloseTime"][:5], "%H:%M").strftime("%I:%M %p")
        storeTiming = f"{storeOpen} to {storeClose}"
        storeNumberRaw = storeCharacteristics["PhoneNumber"]
        storeNumberFormatted = f" • +1 ({storeNumberRaw[:3]}) {storeNumberRaw[3:6]}-{storeNumberRaw[6:]}"
        storeDistance = f"{int(store['DistanceToStoreFromOrigin'])} miles"
        storeSite = " • " + f'<a href=https://www.petsmart.com/ target="_blank">Website</a>'

        popup = folium.Popup(f"<b>Address:</b><br>{storeStreet}<br>{storeDistance} away<br><br><b>Services:</b><br>{storeServices}<br><br><b>Hours:</b><br>{storeTiming}<br><br><b>Contact:</b><br>{storeNumberFormatted}<br>{storeSite}", max_width=300, min_width=150)

        folium.Marker([storeLat, storeLon], popup=popup, tooltip=storeName, icon=folium.Icon(color="blue")).add_to(storeMap)

    data = io.BytesIO()
    storeMap.save("templates/map/map.html")

@app.route("/get-loc/<next>")
def get_loc(next):
    return render_template("get_loc.html", next=next)

@app.route("/save-location", methods=["POST"])
def save_location():
    data = request.get_json()
    session["lat"] = data["lat"]
    session["lng"] = data["lng"]
    return ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if not session.get("lat") or not session.get("lng"):
        return redirect(url_for("get_loc", next="form"))
    if request.method == "POST":
        pet_type = request.form.get("rtype")
        size = request.form.getlist("csize")
        gender = request.form.get("rgender")
        age = request.form.getlist("cage")
        coat = request.form.getlist("ccoat")
        if "medium" in coat and pet_type == "rabbit":
            del coat[coat.index("medium")]
        if "hairless" in coat and pet_type == "rabbit":
            del coat[coat.index("hairless")]
        if "wire" in coat and pet_type == "rabbit":
            del coat[coat.index("wire")]
        if "curly" in coat and pet_type == "rabbit":
            del coat[coat.index("curly")]
        dist = request.form.get("distance")
        gwith = request.form.getlist("cgoodWith")
        session["filters"] = {
            "animal_type": pet_type,
            "size": size if size else None,
            "gender": ["male", "female"] if gender == "both" else gender,
            "age": age if age else None,
            "coat": coat if (coat and coat[0]) else None,
            "lat": session["lat"], 
            "long": session["lng"], 
            "distance": dist,
            "gwca": "gwca" in gwith,
            "gwd": "gwd" in gwith,
            "gwch": "gwch" in gwith
        }
        return redirect(url_for("results"))
    pf = Petfinder(key=ACCESS_TOKEN, secret=SECRET)
    return render_template("form.html")

@app.route("/results")
def results():
    if not session.get("lat") or not session.get("lng"):
        return redirect(url_for("get_loc", next="results"))
    if not session.get("filters"):
        return redirect(url_for("form"))
    animals = get_pets(**session["filters"])
    return render_template("results.html", animals=animals)

@app.route("/map")
def map():
  return render_template("map/map.html")

@app.route("/stores")
def stores():
    if not session.get("lat") or not session.get("lng"):
        return redirect(url_for("get_loc", next="stores"))
    store_map()
    return render_template("store.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")