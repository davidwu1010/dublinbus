import createSagaMiddleware from 'redux-saga';
import { persistStore } from 'redux-persist';

import logger from 'redux-logger';
import rootReducer from './root-reducer';
import rootSaga from './root-saga';
import { createStore, applyMiddleware } from 'redux';

const sagaMiddleware = createSagaMiddleware();
const middlewares = [sagaMiddleware];

if (process.env.NODE_ENV === 'development') {
  middlewares.push(logger);
}

export const store = createStore(rootReducer, applyMiddleware(...middlewares));

sagaMiddleware.run(rootSaga);
export const persistor = persistStore(store);
export default { store, persistStore };