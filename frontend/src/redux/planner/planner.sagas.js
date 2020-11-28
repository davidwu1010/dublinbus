import { takeLatest, put, all, call } from 'redux-saga/effects';

import PlannerActionTypes from './planner.types';
import { autocompleteFailure, autocompleteSuccess, directionsFailure, directionsSuccess } from './planner.actions';
import { setPolylines } from '../map/map.actions';

function* autocomplete({ payload: { input, source } }) {
  if (input === "") {
    yield put(autocompleteSuccess([]));
  } else {
    const service = new window.google.maps.places.AutocompleteService();
    const promise = new Promise((resolve, reject) => {
      service.getPlacePredictions({ input: input, location: new window.google.maps.LatLng({ lat: 53.4321, lng: -6.2759 }), radius: 11000 }, (predictions, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK) {
          resolve(predictions);
        } else {
          reject(status);
        }
      })
    });

    try {
      const response = yield promise;
      const places = response
        .filter(places => places.description.includes('Dublin'));

      yield put(autocompleteSuccess(places, source));
    } catch(error) {
      yield put(autocompleteFailure(error));
    }
  }
}

function* getDirections({ payload: { origin, dest } }) {
  const directionsService = new window.google.maps.DirectionsService();
  const promise = new Promise((resolve, reject) => {
       directionsService.route({origin: origin, destination: dest, travelMode: 'TRANSIT', provideRouteAlternatives: true, transitOptions: {modes: ['BUS']}, region: 'ie'},
         (response, status) => {
            if (status === 'OK') {
              resolve(response);
            } else {
              reject(status);
            }
         });
  });

  try {
    const routes = yield promise;
    yield call(console.log, routes);
    const pathToPolyline = path => path.map(point => ({ lat: point.lat(), lng: point.lng() }));
    yield put(setPolylines(routes.routes.map(route => pathToPolyline(route.overview_path))));
    yield put(directionsSuccess(routes));
  } catch (error) {
    yield put(directionsFailure(error));
  }
}

export function* onAutoCompleteStart() {
  yield takeLatest(PlannerActionTypes.AUTOCOMPLETE_START, autocomplete);
}

export function* onDirectionsStart() {
  yield takeLatest(PlannerActionTypes.DIRECTIONS_START, getDirections);
}

export function* plannerSagas() {
  yield all([call(onAutoCompleteStart), call(onDirectionsStart)]);
}