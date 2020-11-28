import React, { useEffect, useState } from 'react';

import { Map, Marker, Polyline } from 'google-maps-react';
import { createStructuredSelector } from 'reselect';
import { connect } from 'react-redux';
import { selectHighlighted, selectPolylines } from '../../redux/map/map.selector';

window.apiKey = 'AIzaSyBPyIqf7hOMSCjqSq--50UKiJ9Xzmbssmk';

const containerStyle = {
  position: 'fixed',
  height: '100vh',
  width: '100vw',
  zIndex: -1
};

const center = {
  lat: 53.3363,
  lng: -6.2769
};


function MapContainer(props) {
  const { polylines, highlighted } = props;
  const [location, setLocation] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(position => setLocation(position.coords));
  }, [])

  return(
    <Map google={window.google} containerStyle={containerStyle} initialCenter={center} zoom={13} disableDefaultUI={true}>
      { polylines.map((polyline, index) => <Polyline key={index} path={polyline} zIndex={index === highlighted ? 1 : 0} strokeColor={index === highlighted ? '#669DF6' : '#BBBDBF'} strokeWeight={6} />) }
      { location ? <Marker title="Your Location" position={{lat: location.latitude, lng: location.longitude}} /> : null }
    </Map>
  );
}

const mapStateToProps = createStructuredSelector({
  polylines: selectPolylines,
  highlighted: selectHighlighted
});

const mapDispatchToProps = dispatch => ({
});

export default connect(mapStateToProps, mapDispatchToProps)(MapContainer);
