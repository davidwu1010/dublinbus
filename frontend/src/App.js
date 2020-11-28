import React, { useEffect } from 'react';

import { CssBaseline } from '@material-ui/core';

import Header from './components/header/header.component';
import HomePage from './pages/homepage/homepage.component';
import LeftDrawer from './components/left-drawer/left-drawer.component';
import { Switch, Route, Redirect } from 'react-router-dom';
import SignUp from './pages/sign-up/sign-up.component';
import SignIn from './pages/sign-in/sign-in.component';
import { createStructuredSelector } from 'reselect';
import { selectCurrentUser } from './redux/user/user.selectors';
import { connect } from 'react-redux';
import { checkUserSession } from './redux/user/user.actions';

function App({ currentUser, checkUserSession }) {
  useEffect(() => {
    checkUserSession();
  }, [checkUserSession]);

  return (
    <React.Fragment>
      <CssBaseline />
      <Header />
      <LeftDrawer />
      <Switch>
        <Route exact path="/sign-in" render={() => currentUser ? <Redirect to='/' /> : <SignIn />} />
        <Route exact path="/sign-up" render={() => currentUser ? <Redirect to='/' /> : <SignUp /> } />
        <Route path="/" component={HomePage} />
      </Switch>
    </React.Fragment>
  );
}

const mapStateToProps = createStructuredSelector({
  currentUser: selectCurrentUser
});

const mapDispatchToProps = dispatch => ({
  checkUserSession: () => dispatch(checkUserSession())
});

export default connect(mapStateToProps, mapDispatchToProps)(App);
