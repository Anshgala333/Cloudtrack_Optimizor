from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic
from algorithm.Routing.mapVisual import draw_routes_on_map
from utils.create_distance_matrix import create_distance_matrix
from config.constants import BOX_WEIGHT

import json
import time
from fastapi import BackgroundTasks

def create_data_model(all_data):
    data = {}
    coordinates = all_data["coordinates"]
    data["distance_matrix"] = create_distance_matrix(coordinates)
    # print(data["distance_matrix"])
    data["demands"] = all_data["demands"]
    data["vehicle_capacities"] = all_data["truck_data"]["vehicle_capacities"]
    data["num_vehicles"] = all_data["truck_data"]["num_vehicles"]
    data["depot"] = 0
    return data

def generate_output(data, manager, routing, solution , customer_names , all_data):
   
    final_output = {"message": []}  

    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route = [data["depot"]]  # Start from depot
        total_demand = 0
        stop_sequence = []
        
        while True:
            node_index = manager.IndexToNode(index)

            # If the current node is depot and it's the only stop, break
            if routing.IsEnd(index):break

            if node_index != data["depot"]:
                route.append(node_index)
                stop_sequence.append((node_index, len(stop_sequence) + 1))
                total_demand += data["demands"][node_index]

            index = solution.Value(routing.NextVar(index))

        if not stop_sequence:
            continue  # Skip empty trucks

        truck_type = all_data["truck_dictionary"][vehicle_id]
        box_list = []

        for stop_index, (node, priority) in enumerate(stop_sequence):
            box_count = data["demands"][node]
            for b in range(box_count):
                box_list.append(
                    {
                        "customer_name": customer_names[node],
                        "priority": priority,
                        "weight": 12,
                        "box_number": b + 1,
                    }
                )
        path_list = []
        total_distance = 0
        for i in range(len(route) - 1):
            from_node = route[i]
            to_node = route[i + 1]
            from_lat_long = all_data["coordinates"][from_node]
            to_lat_long = all_data["coordinates"][to_node]
            dist = data["distance_matrix"][from_node][to_node]
            path_list.append({"from": from_lat_long, "to": to_lat_long, "distance": dist})
            total_distance += dist

        truck_data = {
            **truck_type,
            "boxes": box_list,
            "weight": total_demand*BOX_WEIGHT,
            "path": path_list,  # 👈 NEW
            "total_distance": total_distance,
        }
        final_output["message"].append(truck_data)

    with open("final_output.json", "w") as f:
        json.dump(final_output, f, indent=4)
        
    print("Output saved to final_output.json")
    return final_output


def main(all_data):
    data = create_data_model(all_data)
    end_index = len(all_data["coordinates"]) - 1
    
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        #  data["depot"]
        [data["depot"]] * data["num_vehicles"],
        [end_index] * data["num_vehicles"],
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index, 0, data["vehicle_capacities"], True, "Capacity"
    )

    group_candidates = [
        (1, 2),  # SLCHR & SLCHR-02 → 300 + 245 = 545 ✅
        (30, 31),  # KNPR & LKNW-TELIBAGH → 115 + 135 = 250 ✅
        (32, 33),  # ALAMBAGH & LKNW-SITAPUR → 83 + 74 = 157 ✅
    ]
    
    # for i, j  in group_candidates:
    #     idx_i = manager.NodeToIndex(i)
    #     idx_j = manager.NodeToIndex(j)
    #     routing.solver().Add(routing.VehicleVar(idx_i) == routing.VehicleVar(idx_j))

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(2)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        structured_data = generate_output(data, manager, routing, solution , all_data["customer_names"] , all_data)
        print( "got data from google")
        # draw_routes_on_map( data, manager, routing, solution, all_data["coordinates"], "withCapacity.html")
        return structured_data
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()
