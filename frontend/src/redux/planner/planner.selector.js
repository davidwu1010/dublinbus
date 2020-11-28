import { createSelector } from 'reselect';

const selectPlanner = state => state.planner;

export const selectOriginPlaces = createSelector(
  [selectPlanner],
  planner => planner.originList
);

export const selectOriginPredictions = createSelector(
  [selectOriginPlaces],
places => places.map(place => place.description)
);

export const selectDestPlaces = createSelector(
  [selectPlanner],
  planner => planner.destList
);

export const selectDestPredictions = createSelector(
  [selectDestPlaces],
  places => places.map(place => place.description)
);

export const selectOrigin = createSelector(
  [selectPlanner],
  planner => planner.origin
);

export const selectDest = createSelector(
  [selectPlanner],
  planner => planner.dest
);

export const selectDirections = createSelector(
  [selectPlanner] ,
  planner => planner.directions
);

export const selectRoutes = createSelector(
  [selectDirections],
  directions => (directions ? directions.routes : [])
);

export const selectPolylines = createSelector(
  [selectRoutes],
  routes => routes.map(route => route.overview_path.map(path => ({ lat: path.lat(), lng: path.lng() })))
);

export const selectSelectedRoute = createSelector(
  [selectPlanner],
  planner => planner.selectedRoute
);