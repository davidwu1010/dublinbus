import PlannerActionTypes from './planner.types';

export const autocompleteStart = (input, source) => ({
  type: PlannerActionTypes.AUTOCOMPLETE_START,
  payload: { input, source }
});

export const autocompleteSuccess = (places, source) => ({
  type: PlannerActionTypes.AUTOCOMPLETE_SUCCESS,
  payload: { places, source }
});

export const autocompleteFailure = error => ({
  type: PlannerActionTypes.AUTOCOMPLETE_FAILURE,
  payload: error
});

export const setOrigin = origin => ({
  type: PlannerActionTypes.SET_ORIGIN,
  payload: origin
});

export const setDest = dest => ({
  type: PlannerActionTypes.SET_DEST,
  payload: dest
});

export const directionsStart = (origin, dest) => ({
  type: PlannerActionTypes.DIRECTIONS_START,
  payload: {
    origin: origin,
    dest: dest
  }
});

export const directionsSuccess = directions => ({
  type: PlannerActionTypes.DIRECTIONS_SUCCESS,
  payload: directions
});

export const directionsFailure = error => ({
  type: PlannerActionTypes.DIRECTIONS_START,
  payload: error
});

export const switchAutocompleteOptions = () => ({
  type: PlannerActionTypes.SWITCH_AUTOCOMPLETE_OPTIONS
});

export const selectRoute = routeId => ({
  type: PlannerActionTypes.SELECT_ROUTE,
  payload: routeId
});
