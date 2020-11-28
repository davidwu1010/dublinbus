import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store, persistor } from './redux/store';
import { PersistGate } from 'redux-persist/integration/react';
import { MuiPickersUtilsProvider } from '@material-ui/pickers';

import DayjsUtils from '@date-io/dayjs';

ReactDOM.render(
  <Provider store={store}>
    <BrowserRouter>
      <MuiPickersUtilsProvider utils={DayjsUtils}>
      <PersistGate persistor={persistor}>
        <App />
      </PersistGate>
      </MuiPickersUtilsProvider>
    </BrowserRouter>
  </Provider>,
  document.getElementById('root')
);
