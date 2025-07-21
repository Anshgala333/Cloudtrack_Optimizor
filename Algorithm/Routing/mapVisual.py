import folium
from branca.element import Element
from geopy.distance import geodesic
import requests
import time
import os
from branca.element import MacroElement
from jinja2 import Template
from polyline import decode
import json

key = 'AIzaSyD_-DylnZGJXFA4AgWo6XK-qp7eBXqml-U'

os.makedirs("MAPS", exist_ok=True)

location_names = [
    "AGRTLA with box 243", #0
    "SLCHR with box  300",#1
    "SLCHR-02 with box 245",#2
    "SHILLONG with box 104 ",#3
    "GW-3-ADBR with box 232 ",#4
    "SLIGURI with box 58",#5
    "BRPT with box 265",#6
    "BRPT-2 with box 185",#7
    "NALBARI with box 76",#8
    "GWHT with box 343",#9
    "BONGAIGAON with box 120",#10
    "ITNGR with box 234",#11
    "TINSUKIA with box 135",#12
    "TEZPUR with box 109",#13
    "JRHT with box 168",#14
    "DIPHU with box 45",#15
    "GOALPARA with box 20",#16
    "BHANGEL with box 78",#17
    "FBD-2 with box 149",#18
    "BAREILLY (GURUDWARA) with box 204",#19
    "BRLY with box 130",#20
    "BUDAUN-(V2) with box 81",#21
    "BHRCH-2 with box 115",#22
    "SITAPUR with box 108",#23
    "BLRMPR with box 71",#24
    "RAMPUR with box 118",#25
    "LAKHIMPUR with box 120",#26
    "GONDA with box 72",#27
    "HARDOI-(V2) with box 126",#28
    "LUCKNOW(KURSI RAOD) with box 115",#29
    "KNPR with box 135",#30
    "LKNW-TELIBAGH with box 84",#31
    "ALAMBAGH with box 83",#32
    "LKNW-SITAPUR ROAD wih box 74",#33
    "LKNW with box 50",#34
    "JNK PRM with box 55",#35
    "RBRLY with box 137",#36
]


def get_google_route_full(route):
    origin = f"{route[0][0]},{route[0][1]}"
    destination = f"{route[-1][0]},{route[-1][1]}"
    waypoints = "optimize:false|" + "|".join([f"{lat},{lon}" for lat, lon in route[1:-1]])
    
    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={origin}&destination={destination}"
        f"&waypoints={waypoints}"
        f"&key={key}"
    )
    coordinates = []
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        with open("Googleroutes.json" , "w") as f:
            json.dump(res.json(), f, indent=4)
          
        # legs = data["routes"][0]["legs"][0]["steps"]
        legs = data["routes"][0]["legs"]
        overview_polyline = data["routes"][0]["overview_polyline"]["points"]
        total_distance  = sum(x["distance"]["value"] for x in legs)
        total_distance = round(total_distance/1000 , 2)
        print(total_distance  , "kms")
        
        # arr = [x["polyline"]["points"] for x in legs]
        # total_distance = sum([x["distance"]["value"] for  x in legs])
        # total_time = sum([x["duration"]["value"] for  x in legs])
        # print(len(arr))
        
        # total_distance = round(total_distance/1000 , 2)
        # print(total_distance  , "kms")

        # for hash in arr :
        #     decoded = decode(hash)
        #     coordinates.extend(decoded)
        decoded = decode(overview_polyline)
        coordinates.extend(decoded)
        print(len(coordinates))
        
        
        return coordinates,total_distance
    

def get_osrm_route(start, end):
    
    # print("calling ")
    # url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
    # try:
    #     res = requests.get(url)
    #     print(res)
    #     if res.status_code == 200:
    #         coords = res.json()["routes"][0]["geometry"]["coordinates"]
    #         # print(coords)
    #         return [
    #             (lat, lng) for lng, lat in coords
    #         ]  # Convert (lng, lat) to (lat, lng)
    # except Exception as e:
    #     print(f"❌ Failed OSRM route for {start} -> {end}: {e}")
    # return [start, end]  # fallback
    
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start[0]},{start[1]}&destination={end[0]},{end[1]}&key={key}'
    coordinates = []
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
          
        legs = data["routes"][0]["legs"][0]["steps"]
        
        arr = [x["polyline"]["points"] for x in legs]
        total_distance = sum([x["distance"]["value"] for  x in legs])
        total_time = sum([x["duration"]["value"] for  x in legs])
        print(len(arr))
        
        total_distance = round(total_distance/1000 , 2)
        print(total_distance  , "kms")

        for hash in arr :
            decoded = decode(hash)
            coordinates.extend(decoded)
        print(len(coordinates))
        return coordinates
            


def create_info_box(route_data):
    html = '<div style="padding: 10px; font-size: 13px;">'
    html += "<h4>📦 Route Summaries</h4>"
    for i, route_info in enumerate(route_data):
        stops = len(route_info["route"])
        dist = route_info["distance"]
        html += f"<b>Vehicle {i+1}:</b> <p>Stops = {stops-1}, Distance = {dist:.2f} km</p>"
    html += "</div>"

    info_element = MacroElement()
    info_element._template = Template(
        f"""
        {{% macro html(this, kwargs) %}}
        <div style="position: fixed; 
                    top: 10px; left: 10px; 
                    width: 220px; 
                    z-index: 9999; 
                    background-color: white; 
                    border: 2px solid gray; 
                    border-radius: 8px;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.2);">
            {html}
        </div>
        {{% endmacro %}}
    """
    )
    return info_element


def draw_routes_on_map(data, manager, routing, solution, coordinates, htmlFileName):
    
    depot_coord = coordinates[data["depot"]]
    m = folium.Map(location=depot_coord, zoom_start=6)

    css = """
    <style>
        .number {
            font-size: 12px;
            color: white;
            background: black;
            border-radius: 50%;
            text-align: center;
            width: 24px;
            height: 24px;
            line-height: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
    """
    m.get_root().html.add_child(Element(css))

    COLORS = [
        "darkred",
        "darkblue",
        "darkgreen",
        "darkorange",
        "purple",
        "brown",
        "black",
        "gray",
        "midnightblue",
        "maroon",
    ]

    route_data = []  # 🧠 We build this here

    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue

        route = []
        total_dist = 0
        index = routing.Start(vehicle_id)
        stop_num = 1

        fg_route = []
        fg = folium.FeatureGroup(
            name=f"Vehicle {vehicle_id}"
        )  # temporary name, update later
        
        color = COLORS[vehicle_id % len(COLORS)]
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            coord = coordinates[node_index]
            route.append(coord)

            # Marker for this stop
            icon_html = f"<div class='number'>{stop_num}</div>"
            tooltip = (
                location_names[node_index]
                if node_index < len(location_names)
                else f"Stop {stop_num}"
            )
            icon = folium.DivIcon(html=icon_html)
            folium.Marker(location=coord, icon=icon, tooltip=tooltip).add_to(fg)

            # Get next
            next_index = solution.Value(routing.NextVar(index))

            # ✅ Break if next is the end (i.e., we've just added the second-last node)
            if routing.IsEnd(next_index):
                break

            index = next_index
            stop_num += 1

        # ✅ Now handle the final (home/depot) marker
        end_index = solution.Value(routing.NextVar(index))  # The actual End()
        final_index = manager.IndexToNode(end_index)
        final_coord = coordinates[final_index]
        # route.append(final_coord)

        # Add final depot/home marker
        folium.Marker(
            location=final_coord,
            icon=folium.Icon(color="gray", icon="home"),
            tooltip="Depot",
        ).add_to(fg)

        # Draw real road polyline
        # for i in range(len(route) - 1):
        #     path = get_osrm_route(route[i], route[i + 1])
        #     seg_dist = geodesic(route[i], route[i + 1]).km
        #     total_dist += seg_dist

        #     folium.PolyLine(
        #         path, color=color, weight=4, opacity=0.9, tooltip=f"{seg_dist:.1f} km"
        #     ).add_to(fg)
        
        for i in range(len(route) - 1):
            total_dist += geodesic(route[i], route[i + 1]).km
        
        full_path,total_distance = get_google_route_full(route)
        folium.PolyLine(
            full_path,
            color=color,
            weight=4,
            opacity=0.9,
            tooltip=f"{total_distance:.1f} km"
        ).add_to(fg)

        # Save this route's data
        route_data.append(
            {"vehicle_id": vehicle_id, "route": route, "distance": total_dist}
        )

        # ✅ Update FeatureGroup name with route summary
        stops_count = len(route) - 2  # excluding start and end depot
        fg.layer_name = (
            f"Vehicle {vehicle_id} ({stops_count} stops, {total_distance:.1f} km)"
        )
        fg.add_to(m)

    # 🧾 Add Info Panel
    m.get_root().add_child(create_info_box(route_data))

    # ✅ Layer toggle
    folium.LayerControl(collapsed=False).add_to(m)

    # m.save(f"MAPS/{htmlFileName}")
    m.save(f"MAPS/routes.html")
    print("✅ Map saved as toggle_routes_map.html")
