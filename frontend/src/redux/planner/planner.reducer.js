import PlannerActionTypes from './planner.types';

const INITIAL_STATE = {
  originList: [],
  destList: [],
  origin: '',
  dest: '',
  directions: null,
  selectedRoute: 0
};

const plannerReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case PlannerActionTypes.AUTOCOMPLETE_SUCCESS:
      if (action.payload.source === 'origin') {
        return {
          ...state,
          originList: action.payload.places
        }
      } else {
        return {
          ...state,
          destList: action.payload.places
        }
      }
    case PlannerActionTypes.SET_ORIGIN:
      return {
        ...state,
        origin: action.payload
      };
    case PlannerActionTypes.SET_DEST:
      return {
        ...state,
        dest: action.payload
      };
    case PlannerActionTypes.DIRECTIONS_SUCCESS:
      return {
        ...state,
        directions: action.payload
      };
    case PlannerActionTypes.SWITCH_AUTOCOMPLETE_OPTIONS:
      const temp = state.destList;
      return {
        ...state,
        destList: state.originList,
        originList: temp
      };
    case PlannerActionTypes.SELECT_ROUTE:
      return {
        ...state,
        selectedRoute: action.payload
      };
    default:
      return state;
  }
};

export default plannerReducer;
