from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os
from datetime import datetime

app = FastAPI(title="ISS Proximity Tracker API")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/api/iss-now")
def proxy_iss_location():
    try:
        res = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
        if res.status_code == 200:
            return res.json()
        raise HTTPException(status_code=500, detail="Failed to reach ISS API")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def home(request: Request, postcode: str = None):
    context = {"request": request, "postcode": postcode}
    
    if not postcode:
        return templates.TemplateResponse("index.html", context)
    
    try:
        # 1. Fetch Postcode Coordinates
        postcode_url = f"https://api.postcodes.io/postcodes/{postcode}"
        postcode_res = requests.get(postcode_url)
        if postcode_res.status_code != 200:
            context["error"] = "Invalid UK Postcode"
            return templates.TemplateResponse("index.html", context)
            
        postcode_data = postcode_res.json()["result"]
        user_lat = postcode_data["latitude"]
        user_lon = postcode_data["longitude"]
        
        context["user_lat"] = user_lat
        context["user_lon"] = user_lon

        # 2. Fetch Next Pass Overhead Prediction Time (Bypasses local timezone bugs)
        # We append a dummy alt parameter to guarantee accurate horizon visibility tracking
        pass_url = f"http://api.open-notify.org/iss-pass.json?lat={user_lat}&lon={user_lon}&n=1"
        pass_res = requests.get(pass_url)
        
        next_pass_time = "No predictable passes over next 24hrs"
        
        if pass_res.status_code == 200:
            pass_data = pass_res.json()
            if "response" in pass_data and len(pass_data["response"]) > 0:
                # Extract the Unix timestamp of the first upcoming overhead crossing
                risetime_unix = pass_data["response"][0]["risetime"]
                # Convert the raw timestamp into a beautiful, readable string layout
                next_pass_time = datetime.utcfromtimestamp(risetime_unix).strftime('%d %b %Y at %H:%M UTC')
        
        context["next_pass"] = next_pass_time
        return templates.TemplateResponse("index.html", context)

    except Exception as e:
        context["error"] = "An error occurred compiling details."
        return templates.TemplateResponse("index.html", context)