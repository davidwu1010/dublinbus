import { all, call } from 'redux-saga/effects';
import { plannerSagas } from './planner/planner.sagas';
import { userSagas } from './user/user.sagas';

function* rootSaga() {
  yield all([call(plannerSagas), call(userSagas)]);
}

export default rootSaga;