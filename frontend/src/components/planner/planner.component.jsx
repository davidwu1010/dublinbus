import React, { useState } from 'react';
import FormInput from '../form-input/form-input.component';
import Grid from '@material-ui/core/Grid';
import RoutesList from '../routes-list/routes-list.component';
import RouteInput from '../route-input/route-input.component';
import Tab from '@material-ui/core/Tab';
import TabPanel from '@material-ui/lab/TabPanel';
import TabContext from '@material-ui/lab/TabContext';
import TabList from '@material-ui/lab/TabList';
import { connect } from 'react-redux';
import { clearPolylines, setPolylines } from '../../redux/map/map.actions';
import { directionsSuccess } from '../../redux/planner/planner.actions';

function Planner({ clearDirections }) {
  const [value, setValue] = useState("1");

  const handleChange = (event, newValue) => {
    setValue(newValue);
    clearDirections();
  };

  return (
      <TabContext value={value}>
      <TabList onChange={handleChange} variant="fullWidth" textColor="primary">
        <Tab value="1" label="By Stops" />
        <Tab value="2" label="By Places" />
      </TabList>
      <TabPanel value="1" index={0} style={{padding: 0}}>
        <Grid container direction="column" style={{width: '100%'}}>
          <Grid item>
            <RouteInput />
          </Grid>
        </Grid>
      </TabPanel>
        <TabPanel value="2" index={1} style={{padding: 0}} >
          <FormInput />
          <RoutesList />
        </TabPanel>
      </TabContext>
  );
}

const mapDispatchToProps = dispatch => ({
  clearPolylines: () => dispatch(clearPolylines()),
  clearDirections: () => dispatch(directionsSuccess(null))
});

export default connect(null, mapDispatchToProps)(Planner);
