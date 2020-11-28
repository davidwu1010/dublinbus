import DrawerActionTypes from './drawer.types';

const INITIAL_STATE = {
  open: false
};

const drawerReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case DrawerActionTypes.TOGGLE_DRAWER:
      return {
        ...state,
        open: !state.open
      };
    default:
      return state;
  }
}

export default drawerReducer;