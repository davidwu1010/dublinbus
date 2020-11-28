import json
import operator
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

base_path = Path(__file__).parent
stops_by_route_path = (base_path / '../app/data/stops_by_route.json').resolve()


def read_file(path):
    with open(stops_by_route_path, 'r') as f:
        return json.load(f)


def test_read_stops():
    response = client.get("/api/stops/1")
    assert response.status_code == 200, 'read stops failed'
    assert operator.__eq__(read_file(stops_by_route_path)['routes']['1']['outbound'],
                           response.json()['outbound']) == True, "read stops wrong respond"


def test_read_stops_between_origin_dest():
    response = client.get("/api/stops/?route_id=1&origin=226&dest=229")
    assert response.status_code == 200, 'read_stops_between_origin_dest failed'
    correct_res = {
        "stops": [
            {
                "stopNumber": 226,
                "lon": -6.26220046436849,
                "lat": 53.391140564198
            },
            {
                "stopNumber": 228,
                "lon": -6.25971957291393,
                "lat": 53.3918773927815
            },
            {
                "stopNumber": 229,
                "lon": -6.25653643266204,
                "lat": 53.3913995158745
            }
        ]
    }
    assert operator.__eq__(response.json(), correct_res) == True, "read_stops_between_origin_dest wrong respond"


def test_nearest():
    response = client.get("/api/stops/nearest/?lat=53.391140564197&lon=-6.26220046436848&route_id=1")
    assert response.status_code == 200, 'nearest failed'
    correct_res = {
        "stop_id": "226"
    }
    assert operator.__eq__(response.json(), correct_res) == True, "nearest, wrong respond"


def test_prediction():
    response = client.get("/api/predictions/1?origin=226&dest=229&dtime=2020-08-18T13%3A00%3A00")
    assert response.status_code == 200, 'prediction failed'
    assert isinstance(response.json()['travelTime'], float) == True, "prediction, wrong respond"


def test_user_post(headers, payload):
    response_post = client.post("/api/saved/", headers=headers, json=payload)
    assert response_post.json()['code'] == 200, 'user_post failed'


def test_user_get(headers):
    response_get = client.get('/api/saved', headers=headers)
    correct_res = {"routes":[{"routeId":"1","origin":{"stopNumber":226,"address":"Shanard Road","location":"Shanard Avenue"},"dest":{"stopNumber":229,"address":"Shanliss Rd","location":"Oldtown Road"}}]}
    assert response_get.status_code == 200, 'user_get failed'
    assert operator.__eq__(response_get.json(), correct_res) == True, "user_get wrong res"


def test_user_delete(headers):
    response_delete = client.delete('/api/saved/?route_id=1&origin=226&dest=229', headers=headers)
    assert response_delete.json()["code"] == 200, 'user_delete failed'


def test_user():
    payload = {
        "route_id": "1",
        "origin": "226",
        "dest": "229",
    }
    headers = {
        'Authorization': 'Bearer TEST',
        }
    test_user_post(headers, payload)
    test_user_get(headers)
    test_user_delete(headers)


def test_main():
    test_read_stops()
    test_read_stops_between_origin_dest()
    test_nearest()
    test_prediction()
    test_user()


if __name__ == "__main__":
    print('Start...')
    test_main()
    print('Done!')