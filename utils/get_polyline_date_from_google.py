import requests
import json
from datetime import datetime
from config.config import settings

API_KEY = settings.google_api_key
URL = settings.GOOGLE_API_FOR_POLYLINE




def get_polyline_date_from_google(structured_output):
    print("call")
    polyline_map = []
    for items in structured_output["message"]:
        path = items["path"]
        # generate origin
        origin_lat, origin_lng = path[0]["from"]

        # generate destination
        dest_lat, dest_lng = path[-1]["to"]

        # generate intermediate
        intermediates = []
        for p in path[:-1]:
            lat, lng = p["to"]
            intermediates.append(
                {"location": {"latLng": {"latitude": lat, "longitude": lng}}}
            )
        request_body = {
            "origin": {
                "location": {
                    "latLng": {"latitude": origin_lat, "longitude": origin_lng}
                }
            },
            "destination": {
                "location": {"latLng": {"latitude": dest_lat, "longitude": dest_lng}}
            },
            "intermediates": intermediates,
            "travelMode": "DRIVE",
            # "departureTime": datetime.utcnow().isoformat() + "Z",
            "polylineEncoding": "ENCODED_POLYLINE",
        }
        
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "*"
        }
        response = requests.post(URL, headers=headers, json=request_body)
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            
        data = response.json()
        route = data["routes"][0]
        
        custom_route = {
            "polyline": [route["polyline"]["encodedPolyline"]],
            "totalDistance": route.get("distanceMeters", 0),
            "totalDuration": route.get("duration", {}),
            "steps": []
        }
        
        for leg in route.get("legs", []):
            step = {
                "from": [
                    leg["startLocation"]["latLng"]["latitude"],
                    leg["startLocation"]["latLng"]["longitude"]
                ],
                "to": [
                    leg["endLocation"]["latLng"]["latitude"],
                    leg["endLocation"]["latLng"]["longitude"]
                ],
                "distance": leg.get("distanceMeters", 0),
                "duration": leg.get("duration", {})
            }
            custom_route["steps"].append(step)
        
        polyline_map.append(custom_route)
            
        with open("ansh1.json", "w") as f:
             json.dump(polyline_map, f, indent=4)

        print("✅ Route saved to ansh1.json")
    return True, polyline_map