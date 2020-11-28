import React, { useEffect, useState } from 'react';
import { auth } from '../../firebase/firebase.utils';
import axios from 'axios';
import { createStructuredSelector } from 'reselect';
import { selectCurrentUser } from '../../redux/user/user.selectors';
import { connect } from 'react-redux';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import { DateTimePicker } from '@material-ui/pickers';
import Divider from '@material-ui/core/Divider';
import { clearPolylines, setPolylines } from '../../redux/map/map.actions';
import SavedRouteItem from '../saved-route-item/saved-route-item.component';
import dayjs from 'dayjs';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import Dialog from '@material-ui/core/Dialog';

const SavedRoutesList = ({ currentUser, clearPolylines }) => {
  const [savedRoutes, setSavedRoutes] = useState([]);
  const [departureTime, setDepartureTime] = useState(new dayjs());
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogContent, setDialogContent] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const token = await auth.currentUser.getIdToken(true);
      const response = await axios.get('/api/saved/', {
        headers: {
          Authorization: 'Bearer' + ' ' + token
        }
      });
      const routes = response.data;
      setSavedRoutes(routes.routes);
    };
    if (currentUser) {
      fetchData();
    }

    return clearPolylines;
  }, [currentUser]);


  return (
    currentUser
      ?
      <>
        <List>
          <ListItem>
            <DateTimePicker
              inputVariant="outlined"
              label="Depart at"
              style={{ width: '100%' }}
              value={departureTime}
              onChange={date => setDepartureTime(date)}
            />
          </ListItem>
          <Divider />
          {
            savedRoutes.map((route, index) =>
              <SavedRouteItem
                key={index}
                departureTime={departureTime}
                setDialogOpen={setDialogOpen}
                setDialogContent={setDialogContent}
                deleteRoute={() => setSavedRoutes(savedRoutes.filter((value, key) => index !== key))}
                {...route} />
                )
          }
        </List>
        <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
          <DialogTitle>Travel time estimation</DialogTitle>
          <DialogContent style={{textAlign: 'center'}}>
            <DialogContentText variant="h5">{ dialogContent }</DialogContentText>
          </DialogContent>
        </Dialog>
      </>
      :
      <Grid container direction="column" alignItems="center" justify="center" style={{ height: '100%' }}>
        <Grid item>
          <Typography variant="h6">Sign in to see saved routes</Typography>
        </Grid>
        <Grid item>
          <Button color="primary" variant="contained" component={Link} to="/sign-in">Sign In</Button>
        </Grid>
      </Grid>
  );
};

const mapStateToProps = createStructuredSelector({
  currentUser: selectCurrentUser
});

const mapDispatchToProps = dispatch => ({
  clearPolylines: () => dispatch(clearPolylines())
});

export default connect(mapStateToProps, mapDispatchToProps)(SavedRoutesList);
