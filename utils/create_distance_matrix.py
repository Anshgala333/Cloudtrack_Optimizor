import math
import asyncio
import aiohttp
import time
import numpy as np

from config.config import settings

API_KEY = settings.google_api_key
MAX_ELEMENTS = 100
SYMMETRIC = True

# Converts (lat, lng) tuples to "lat,lng" strings
def format_locations(location_tuples):
    return [f"{lat},{lng}" for lat, lng in location_tuples]


# Extracts distance matrix from Google API JSON response
def extract_distances(response):
    rows = response.get("rows", [])
    return [
        [elem.get("distance", {}).get("value", -1) for elem in row.get("elements", [])]
        for row in rows
    ]


# Async Google Distance Matrix fetch
async def fetch_matrix(session, origins, destinations, oi_start, dj_start, matrix, symmetric):
    origin_str = "|".join(origins)
    destination_str = "|".join(destinations)

    url = (
        "https://maps.googleapis.com/maps/api/distancematrix/json?"
        f"origins={origin_str}&destinations={destination_str}&key={API_KEY}&units=metric"
    )

    async with session.get(url) as resp:
        data = await resp.json()

        if data.get("status") != "OK":
            # return 
            return

        chunk = extract_distances(data)
        for oi, row in enumerate(chunk):
            for dj, val in enumerate(row):
                i = oi_start + oi
                j = dj_start + dj
                matrix[i][j] = val
                if symmetric and i != j:
                    matrix[j][i] = val



async def compute_distance_matrix_async(locations, max_elements=MAX_ELEMENTS, symmetric=SYMMETRIC):
    N = len(locations)
    matrix = [[-1] * N for _ in range(N)]
    max_chunk = int(math.floor(math.sqrt(max_elements)))

    chunks = [(i, min(i + max_chunk, N)) for i in range(0, N, max_chunk)]

    async with aiohttp.ClientSession() as session:
        tasks = []

        for i, (oi_start, oi_end) in enumerate(chunks):
            origins_chunk = locations[oi_start:oi_end]

            for j, (dj_start, dj_end) in enumerate(chunks):
                if symmetric and j < i:
                    continue

                destinations_chunk = locations[dj_start:dj_end]

                # print(f"🔄 Launching task for origins {oi_start}-{oi_end-1} to destinations {dj_start}-{dj_end-1}")
                task = fetch_matrix(
                    session,
                    origins_chunk,
                    destinations_chunk,
                    oi_start,
                    dj_start,
                    matrix,
                    symmetric,
                )
                tasks.append(task)

        await asyncio.gather(*tasks)

    return matrix



def create_distance_matrix(location_tuples):
    locations = format_locations(location_tuples)
    matrix = asyncio.run(compute_distance_matrix_async(locations))
    np_arr = np.array(matrix)
    np_arr_divideby_1000 = (np_arr // 1000).astype(int)
    return np_arr_divideby_1000.tolist()