import json 

with open("list_of_stations.json" , "r") as f :
    data = json.load(f) 

req_data = ""
for station in data :
    req_data += station["station_name"] + "\n"

with open("list_of_stations.txt", "w") as f :
    f.write(req_data)
