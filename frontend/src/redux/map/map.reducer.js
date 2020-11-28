import mapActionTypes from './map.types';

const INITIAL_STATE = {
  polylines: [],
  highlighted: 0
};

const mapReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case mapActionTypes.SET_POLYLINES:
      return {
        ...state,
        polylines: action.payload
      };
    case mapActionTypes.HIGHLIGHT_POLYLINE:
      return {
        ...state,
        highlighted: action.payload
      }
    case mapActionTypes.CLEAR_POLYLINES:
      return {
        ...state,
        highlighted: 0,
        polylines: []
      }
    default:
      return state;
  }
};

export default mapReducer;