
import time
from utils.validator import validate
from utils.cleaner import cleanse_data
from utils.get_order import get_order
from utils.get_coordinates import get_coordinates
from utils.get_customer_names import get_customer_names
from utils.get_truck_types import get_truck_types
from utils.vehicle_data_as_per_google import vehicle_details_as_per_google
from algorithm.Routing.map_with_capacity import main as get_data_from_google_or_tools
from utils.get_polyline_date_from_google import get_polyline_date_from_google
from utils.get_beautified_output import get_beautified_output
from config.logger import logger


def optimize(file_path):
    
    start = time.perf_counter()

    # step 1:- validate excel file
    is_valid, message = validate(file_path)
    if not is_valid:
        print("valid error", message)
        return message
    logger.info("validated data")

    # step 2:- clean the data
    cleanse_data(file_path)
    logger.info("cleaned data")
    

    # step 3:- get orders of each customer
    status, demands = get_order(file_path)
    if not status:
        print("demand error", demands)
        return demands
    # print(demands)

    # step 4:- get array of co-ordinates
    status, coordinates = get_coordinates(file_path)
    if not status:
        print("coordinates error", demands)
        return coordinates
    # print(coordinates)

    # step 5:- get customer name
    status, customer_names = get_customer_names(file_path)
    if not status:
        print("customer error", customer_names)
        return customer_names
    # print(customer_names)

    # step 6:- grouping of data
    truck_types = get_truck_types(file_path)

    # step 7:- formating of truck data as per google requirements
    truck_data, dictionary = vehicle_details_as_per_google(truck_types)
    # print(truck_data)
    # print(dictionary)
    
    
    
    # step 8 :- run google or tools algo and get truck with their routes
    all_data = {
        "demands": demands,
        "coordinates": coordinates,
        "customer_names": customer_names,
        "truck_data": truck_data,
        "truck_dictionary": dictionary,
    }
    structured_output = get_data_from_google_or_tools(all_data)
    
    
    #step 8 :- this function returns the required thing for plotting the route trajectory on map
    polyline_status , polyline_data_for_plotting = get_polyline_date_from_google(structured_output)
    print(polyline_status)
    
    
    #step 9 :- get 3d positioned data and assemble all data
    beautified_output = get_beautified_output(structured_output)
    
    
    
    print(time.perf_counter()-start)
    


if __name__ == "__main__":
    optimize(
        r"C:\Users\ANSH\Desktop\CloudTrack Optimizor\FastApi CSV\uploads\1752841971.5697021_test.xlsx"
    )
