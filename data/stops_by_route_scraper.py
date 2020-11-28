import requests
import xmltodict
from bs4 import BeautifulSoup
import json

stops_53a = {
    'outbound': [{"stopNumber": "1172", "address": "Gardiner Street",
                  "location": "Railway Street"},
                 {"stopNumber": "4380", "address": "Talbot Street",
                  "location": "Gardiner Street"},
                 {"stopNumber": "4509", "address": "Summerhill",
                  "location": "Sean O'Casey Ave"},
                 {"stopNumber": "7705", "address": "Sheriff Street Upper",
                  "location": "Castleforbes Road"},
                 {"stopNumber": "7708", "address": "Portland Row",
                  "location": "Amiens Street"},
                 {"stopNumber": "7709", "address": "Seville Place",
                  "location": "Sheriff Street Upper"},
                 {"stopNumber": "7710", "address": "Sheriff Street Upper",
                  "location": "Railway Station"},
                 {"stopNumber": "7711", "address": "Sheriff Street Upper",
                  "location": "Castleforbes Road"}],
    'inbound': [{"stopNumber": "512", "address": "Summerhill Rd",
                 "location": "Mountview Court"},
                {"stopNumber": "513", "address": "Summerhill Rd",
                 "location": "Rutland Street"},
                {"stopNumber": "4380", "address": "Talbot Street",
                 "location": "Gardiner Street"},
                {"stopNumber": "6251", "address": "Sheriff Street",
                 "location": "Railway Station"},
                {"stopNumber": "7402", "address": "Gardiner Street",
                 "location": "Talbot St"},
                {"stopNumber": "7705", "address": "Sheriff Street Upper",
                 "location": "Castleforbes Road"},
                {"stopNumber": "7706", "address": "Seville Place",
                 "location": "Sheriff Street Upper"},
                {"stopNumber": "7707", "address": "Portland Row",
                 "location": "Summerhill Rd"}]
}


def split_sub_routes(route):
    if '/' in route:
        number, letter = route.split('/')
        return number, number + letter
    else:
        return (route,)


def fetch_stations(route, direction):
    url = 'https://www.dublinbus.ie/Labs.EPiServer/GoogleMap/gmap_conf.aspx'
    payload = {'custompageid': 1219,
               'action': 'GetStops',
               'routeNumber': route,
               'direction': direction
               }
    response = requests.get(url, params=payload)
    if response.headers.get('content-type') == 'text/xml':
        data_dict = xmltodict.parse(response.text[3:], encoding='utf-8')
        stop_numbers = map(lambda poi:
                           {'stopNumber': poi.get('stopnumber'),
                            'address': poi.get('address'),
                            'location': poi.get('location')
                            },
                           data_dict.get('gmap').get('data').get('poi'))
        return list(stop_numbers)
    else:
        return []


response = requests.get('https://www.dublinbus.ie/Your-Journey1/Timetables/')
soup = BeautifulSoup(response.text, 'html.parser')

routes = soup.findAll('td', class_='RouteNumberColumn')
routes = map(lambda route: route.a.text.strip(), routes)
routes = map(lambda route: split_sub_routes(route), routes)

route_list = []
for route in routes:
    route_list.extend(route)

stops_by_route = {}
empty_routes = []
for route in route_list:
    outbound_stops = fetch_stations(route, 'O')
    inbound_stops = fetch_stations(route, 'I')
    if len(outbound_stops) != 0 or len(inbound_stops) != 0:
        stops_by_route[route] = {'outbound': outbound_stops,
                                 'inbound': inbound_stops}
    else:
        empty_routes.append(route)
        if route == '53a':
            stops_by_route['53a'] = stops_53a
    print(f'{len(stops_by_route) + len(empty_routes)}/{len(route_list)}')

print(empty_routes)

with open('stops_by_route.json', 'w') as file:
    json.dump({'routes': stops_by_route}, file, indent=2)
