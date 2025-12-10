import os
import json

curr_path = os.path.dirname(__file__)


def cache_results(train_num: str, station: str) -> dict:
    """Searches for the cached results for a given train number and station."""

    output = {
        "is_avaliable": False,
        "data": None,
    }

    is_train_avaliable = os.path.isdir(os.path.join(curr_path, "cache",train_num))

    if is_train_avaliable:
        avaliable_stations = os.listdir(os.path.join(curr_path,"cache",train_num))
        for avaliable_station in avaliable_stations:
            if station.lower() in avaliable_station.lower() :
                output["is_avaliable"] = True
                file_loc = os.path.join(
                    curr_path, "cache", train_num,avaliable_station)
                with open(file_loc,"r") as f:
                    output["data"] = json.load(f)
    return output

def save_cache(cache_output : dict ) :
    """save cache will actually update the cache files not rewrite them"""
    train_folder = os.path.join(curr_path,"cache",cache_output["train-no"])
    try :
        os.mkdir(train_folder)
    except Exception as e :
        print("Folder Exists , updating files... ")

    for station,station_data in cache_output["each_station_data"].items()  : 
        try :
            with open(os.path.join(train_folder,f"{station}.json"),"r") as f:
                existing_data = json.load(f)
            
            existing_data.update(station_data)
        except:
            existing_data = station_data
        
        with open(os.path.join(train_folder,f"{station}.json"),"w") as f:
            json.dump(existing_data,f,indent=4)

if __name__ == "__main__":
    cache_results("12749", "lingampalli")
