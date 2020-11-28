import { combineReducers } from 'redux';
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

import plannerReducer from './planner/planner.reducer';
import drawerReducer from './drawer/drawer.reducer';
import userReducer from './user/user.reducer';
import mapReducer from './map/map.reducer';

const persistConfig = {
  key: 'dublinbus',
  storage,
  whitelist: []
}

const rootReducer = combineReducers({
  planner: plannerReducer,
  drawer: drawerReducer,
  user: userReducer,
  map: mapReducer
});

export default persistReducer(persistConfig, rootReducer);
