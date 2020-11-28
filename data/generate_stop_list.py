import json

with open('sections.json', 'r') as input_file:
    sections = json.load(input_file)['sections']
    stops = set()
    for section in sections:
        stop1, stop2 = section.split('-')
        stops.add(stop1)
        stops.add(stop2)

    stops = sorted(list(stops), key=lambda stop: int(stop))

    with open('stops.json', 'w') as output_file:
        json.dump({'stops': stops}, output_file, indent=2)
