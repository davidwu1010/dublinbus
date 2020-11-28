import React from 'react';
import MapContainer from '../../components/map-container/map-container.component';
import Hidden from '@material-ui/core/Hidden';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import Planner from '../../components/planner/planner.component';
import { Switch, Route, useLocation } from 'react-router-dom';
import SavedRoutesList from '../../components/saved-routes-list/saved-routes-list.component';

const useStyles = makeStyles(theme => ({
  paperContainer: {
    background: 'white',
    position: 'fixed',
    width: '400px',
    height: 'calc(100% - 64px)',
    overflowX: 'hidden',
    overflowY: 'auto',
    [theme.breakpoints.down('xs')]: {
      position: 'relative',
      width: '100%',
      height: 'calc(100vh - 56px)',
      overflow: 'visible'
    }
  }
}));

function HomePage(props) {
  const classes = useStyles();
  const location = useLocation();
  return (
    <React.Fragment>
      <div className={classes.paperContainer}>
        { location.pathname === '/saved'
          ?
          <SavedRoutesList />
          :
          <Planner />
        }
      </div>
      <Hidden xsDown>
        <MapContainer />
      </Hidden>
    </React.Fragment>
  );
}

export default HomePage;