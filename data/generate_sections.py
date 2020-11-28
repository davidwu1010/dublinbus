import json

sections = set()
with open('stops_by_route.json', 'r') as input_file:
    data = json.load(input_file)
    routes = data['routes'].values()
    for route in routes:
        outbound = route['outbound']
        inbound = route['inbound']

        for i in range(len(outbound) - 1):
            origin = outbound[i]['stopNumber']
            dest = outbound[i+1]['stopNumber']
            sections.add(f'{origin}-{dest}')
        for i in range(len(inbound) - 1):
            origin = inbound[i]['stopNumber']
            dest = inbound[i+1]['stopNumber']
            sections.add(f'{origin}-{dest}')

    with open('sections.json', 'w') as output_file:
        json.dump({'sections': list(sections)}, output_file, indent=2)
