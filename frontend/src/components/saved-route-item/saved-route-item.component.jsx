import React from 'react';
import ListItemText from '@material-ui/core/ListItemText';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import IconButton from '@material-ui/core/IconButton';
import DirectionsIcon from '@material-ui/icons/Directions';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import ListItem from '@material-ui/core/ListItem';
import axios from 'axios';
import { connect } from 'react-redux';
import { setPolylines } from '../../redux/map/map.actions';
import Grid from '@material-ui/core/Grid';
import { auth } from '../../firebase/firebase.utils';

const SavedRouteItem = ({ routeId, origin, dest, departureTime, setPolylines, setDialogOpen, setDialogContent, deleteRoute }) => {
  const handleClick = event => {
    axios.get('/api/predictions/' + routeId, {
      params: {
        origin: origin.stopNumber,
        dest: dest.stopNumber,
        dtime: departureTime.format('YYYY-MM-DD HH:mm:ss')
      }
    })
      .then(response => {
          setDialogContent(Math.trunc(Math.ceil(response.data.travelTime / 60)) + ' mins');
          setDialogOpen(true);
          })
      .catch(error => console.log(error));

    axios.get('/api/stops/', {
      params: {
        route_id: routeId,
        origin: origin.stopNumber,
        dest: dest.stopNumber
      }
    })
      .then(async response => {
        const stopsCoordinates = response.data.stops.map(stop => stop.lat + ',' + stop.lon);
        const snapResponse = await axios.get('https://roads.googleapis.com/v1/snapToRoads', {
          params: {
            path: stopsCoordinates.join('|'),
            key: window.apiKey,
            interpolate: true
          }
        });
        setPolylines([snapResponse.data.snappedPoints.map(({ location }) => ({
          lat: location.latitude,
          lng: location.longitude
        }))]);
      })
      .catch(error => console.log(error));
  };

  const handleDelete = async event => {
    try {
      const token = await auth.currentUser.getIdToken(true);
      const response = await axios.delete('/api/saved/', {
        params: {
          route_id: routeId,
          origin: origin.stopNumber,
          dest: dest.stopNumber
        },
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
    } catch(error) {
      console.log(error);
    }
    deleteRoute();
  };

  return (
    <ListItem>
      <ListItemText>
        <Card>
          <CardContent style={{ marginRight: '20px' }}>
            <Typography variant="h4">{routeId}</Typography>
            <Typography
              variant="h6">{'Origin: ' + [origin.address, origin.location, 'Stop ' + origin.stopNumber].join(', ')}</Typography>
            <Typography
              variant="h6">{'Dest: ' + [dest.address, dest.location, 'Stop ' + dest.stopNumber].join(', ')}</Typography>
          </CardContent>
        </Card>
        <ListItemSecondaryAction>
          <Grid container direction="column">
            <Grid item>
              <IconButton onClick={handleClick}>
                <DirectionsIcon color="primary" fontSize="large" />
              </IconButton>
            </Grid>
            <Grid item>
              <IconButton onClick={handleDelete}>
                <DeleteForeverIcon color="primary" fontSize="large" />
              </IconButton>
            </Grid>
          </Grid>
        </ListItemSecondaryAction>
      </ListItemText>
    </ListItem>
  );
};

const mapDispatchToProps = dispatch => ({
  setPolylines: polylines => dispatch(setPolylines(polylines))
});

export default connect(null, mapDispatchToProps)(SavedRouteItem);