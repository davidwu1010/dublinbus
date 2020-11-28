import React, { useEffect, useState } from 'react';
import Card from '@material-ui/core/Card';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import { Autocomplete } from '@material-ui/lab';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import clsx from 'clsx';
import axios from 'axios';
import * as dayjs from 'dayjs';
import { DateTimePicker } from '@material-ui/pickers';
import Typography from '@material-ui/core/Typography';
import { connect } from 'react-redux';
import { clearPolylines, setPolylines } from '../../redux/map/map.actions';
import { auth } from '../../firebase/firebase.utils';
import { createStructuredSelector } from 'reselect';
import { selectCurrentUser } from '../../redux/user/user.selectors';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogActions from '@material-ui/core/DialogActions';
import { Link } from 'react-router-dom';


const useStyles = makeStyles({
  card: {
    padding: '16px 0'
  },
  input: {
    width: '340px',
  },
  submitButton: {
    height: '56px'
  }
});

function RouteInput({ setPolylines, clearPolylines }) {
  const classes = useStyles();
  const [routeOptions, setRouteOptions] = useState([]);
  const [originOptions, setOriginOptions] = useState([]);
  const [destOptions, setDestOptions] = useState([]);
  const [route, setRoute] = useState('');
  const [origin, setOrigin] = useState('');
  const [dest, setDest] = useState('');
  const [stops, setStops] = useState({ outbound: [], inbound: [] });
  const [departureTime, setDepartureTime] = useState(new dayjs());
  const [travelTime, setTravelTime] = useState(null);
  const [confirmationOpen, setConfirmationOpen] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        const response = await axios.get('/api/routes/');
        setRouteOptions(response.data.routes || []);
      } catch (error) {
        console.log(error);
      }
    };
    fetchRoutes();
    return clearPolylines;
  }, []);

  useEffect(() => {
    if (!route) {
      setOriginOptions([]);
      return;
    }

    const fetchStops = async () => {
      try {
        const response = await axios.get('/api/stops/' + route);
        const stops = response.data;
        setStops(stops);
        const allStops = new Set();
        stops.outbound.map(stop => [stop.address, stop.location, 'Stop ' + stop.stopNumber].join(', ')).forEach(stop => allStops.add(stop));
        stops.inbound.map(stop => [stop.address, stop.location, 'Stop ' + stop.stopNumber].join(', ')).forEach(stop => allStops.add(stop));
        setOrigin('');
        setOriginOptions(Array.from(allStops));
      } catch (error) {
        console.log(error);
      }
    };
    fetchStops();
  }, [route]);

  useEffect(() => {
    let destList = new Set();
    const outboundStops = stops.outbound.map(stop => [stop.address, stop.location, 'Stop ' + stop.stopNumber].join(', '));
    const inboundStops = stops.inbound.map(stop => [stop.address, stop.location, 'Stop ' + stop.stopNumber].join(', '));
    let index = outboundStops.indexOf(origin);
    if (index !== -1) {
      outboundStops.slice(index + 1).forEach(stop => destList.add(stop));
    }

    index = inboundStops.indexOf(origin);
    if (index !== -1) {
      inboundStops.slice(index + 1).forEach(stop => destList.add(stop));
    }
    destList = Array.from(destList);
    setDestOptions(destList);
  }, [origin]);

  const handleSubmit = async event => {
    event.preventDefault();
    const originStopNumber = origin.split(', ').pop().replace('Stop ', '');
    const destStopNumber = dest.split(', ').pop().replace('Stop ', '');
    axios.get('/api/predictions/' + route, {
      params: {
        origin: originStopNumber,
        dest: destStopNumber,
        dtime: departureTime.format('YYYY-MM-DD HH:mm:ss')
      }
    })
      .then(response => setTravelTime(Math.trunc(Math.ceil(response.data.travelTime / 60))))
      .catch(error => console.log(error));
    axios.get('/api/stops/', {
      params: {
        route_id: route,
        origin: originStopNumber,
        dest: destStopNumber
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
        setPolylines([snapResponse.data.snappedPoints.map(({ location }) => ({ lat: location.latitude, lng: location.longitude }))]);
      })
      .catch(error => console.log(error));
  };

  const handleClick = async event => {
    if (auth.currentUser) {
      const token = await auth.currentUser.getIdToken(true);
      const originStopNumber = origin.split(', ').pop().replace('Stop ', '');
      const destStopNumber = dest.split(', ').pop().replace('Stop ', '');
      try {
        const response = await axios.post('/api/saved/', {
           route_id: route,
           origin: originStopNumber,
           dest: destStopNumber
        }, {
          headers: {
            Authorization: "Bearer " + token
          }
        });
      } catch (error) {
        console.log(error);
      }
      setConfirmationOpen(true);
    } else {
      setDialogOpen(true);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Card variant="outlined" className={classes.card}>
        <Grid container direction="column" alignItems="center" spacing={1}>
          <Grid item>
            <Autocomplete
              renderInput={params => <TextField {...params} label="Route" variant="outlined" required />}
              options={routeOptions}
              className={classes.input}
              onChange={(event, value) => {
                setRoute(value);
                setOrigin('');
                setDest('');
              }}
              autoComplete
              autoHighlight
              autoSelect
            />
          </Grid>
          <Grid item>
            <Autocomplete
              renderInput={params => <TextField {...params} label="Origin" variant="outlined" required />}
              options={originOptions}
              className={classes.input}
              onChange={(event, value) => {
                setOrigin(value || '');
                setDest('');
              }}
              autoComplete
              autoHighlight
              autoSelect
              value={origin}
            />
          </Grid>
          <Grid item>
            <Autocomplete
              renderInput={params => <TextField {...params} label="Destination" variant="outlined" required />}
              options={destOptions}
              className={classes.input}
              onChange={(event, value) => {
                setDest(value || '');
              }}
              autoComplete
              autoHighlight
              autoSelect
              value={dest}
            />
          </Grid>
          <Grid item>
            <DateTimePicker
              inputVariant="outlined"
              label="Depart at"
              onChange={date => setDepartureTime(date)}
              value={departureTime}
              className={classes.input}
              required
            />
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              color="primary"
              className={clsx(classes.input, classes.submitButton)}
              type="submit"
            >
              Submit
            </Button>
          </Grid>
          {travelTime ?
            <>
              <Grid item>
                <Typography variant="h2">{travelTime + ' mins'}</Typography>
              </Grid>
              <Grid item>
                <Button variant="contained" color="secondary" onClick={handleClick}>
                  Save
                </Button>
                <Dialog open={confirmationOpen} onClose={() => setConfirmationOpen(false)}>
                  <DialogContent>
                    <DialogContentText>Saved!</DialogContentText>
                  </DialogContent>
                </Dialog>
                <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
                  <DialogTitle>Sign In?</DialogTitle>
                  <DialogContent>
                    <DialogContentText>You have to sign in first to save routes.</DialogContentText>
                  </DialogContent>
                  <DialogActions>
                    <Button color="primary" onClick={() => setDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button color="primary" component={Link} to="/sign-in">
                      Sign In
                    </Button>
                  </DialogActions>
                </Dialog>
              </Grid>
            </>
            : null
          }
        </Grid>
      </Card>
    </form>
  );
}

const mapDispatchToProps = dispatch => ({
  setPolylines: polylines => dispatch(setPolylines(polylines)),
  clearPolylines: () => dispatch(clearPolylines())
});

const mapStateToProps = createStructuredSelector({
  currentUser: selectCurrentUser
});

export default connect(mapStateToProps, mapDispatchToProps)(RouteInput);
