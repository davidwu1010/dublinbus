import mapActionTypes from './map.types';

export const setPolylines = polylines => ({
  type: mapActionTypes.SET_POLYLINES,
  payload: polylines
});

export const highlightPolyline = polylineId => ({
  type: mapActionTypes.HIGHLIGHT_POLYLINE,
  payload: polylineId
});

export const clearPolylines = () => ({
  type: mapActionTypes.CLEAR_POLYLINES
})
