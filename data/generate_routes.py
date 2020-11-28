import json

with open('stops_by_route.json', 'r') as input_file:
    data = json.load(input_file)
    routes = list(data['routes'].keys())
    with open('routes.json', 'w') as output_file:
        json.dump({'routes': routes}, output_file, indent=2)
