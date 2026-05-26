from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from geopy.distance import geodesic
import os

app = FastAPI(title="ISS Proximity Tracker API")

# Setup the template directory path safely
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/", response_class=HTMLResponse)
def home(request: Request, postcode: str = None):
    # If no postcode is submitted yet, just render the blank form page
    if not postcode:
        return templates.TemplateResponse("index.html", {"request": request})
    
    try:
        # 1. Fetch Postcode Coordinates from api.postcodes.io
        postcode_url = f"https://api.postcodes.io/postcodes/{postcode}"
        postcode_res = requests.get(postcode_url)
        if postcode_res.status_code != 200:
            return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid UK Postcode", "postcode": postcode})
            
        postcode_data = postcode_res.json()["result"]
        user_location = (postcode_data["latitude"], postcode_data["longitude"])

        # 2. Fetch Live ISS Location from open-notify.org
        iss_url = "http://api.open-notify.org/iss-now.json"
        iss_res = requests.get(iss_url)
        if iss_res.status_code != 200:
            return templates.TemplateResponse("index.html", {"request": request, "error": "Failed to get live ISS data", "postcode": postcode})
            
        iss_data = iss_res.json()["iss_position"]
        iss_location = (float(iss_data["latitude"]), float(iss_data["longitude"]))

        # 3. Calculate geodesic distance in kilometers
        distance_km = geodesic(user_location, iss_location).kilometers
        is_overhead = distance_km < 800.0  # Visible overhead if within 800km

        # Pass all the live calculated numbers into the HTML file
        return templates.TemplateResponse("index.html", {
            "request": request,
            "postcode": postcode.upper(),
            "distance_km": round(distance_km, 2),
            "is_visible_overhead": is_overhead,
            "iss_lat": round(iss_location[0], 4),
            "iss_lon": round(iss_location[1], 4)
        })

    except Exception:
        return templates.TemplateResponse("index.html", {"request": request, "error": "An unexpected network error occurred."})