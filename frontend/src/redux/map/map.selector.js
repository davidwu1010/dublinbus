import { createSelector } from 'reselect';

const selectMap = state => state.map;

export const selectPolylines = createSelector(
  [selectMap],
  map => map.polylines
);

export const selectHighlighted = createSelector(
  [selectMap],
  map => map.highlighted
);
