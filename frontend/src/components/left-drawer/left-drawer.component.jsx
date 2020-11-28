import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import SwipeableDrawer from '@material-ui/core/SwipeableDrawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import { createStructuredSelector } from 'reselect';
import { connect } from 'react-redux';
import { selectDrawerOpen } from '../../redux/drawer/drawer.selectors';
import { toggleDrawer } from '../../redux/drawer/drawer.action';
import BookmarksIcon from '@material-ui/icons/Bookmarks';
import DirectionsBusIcon from '@material-ui/icons/DirectionsBus';
import { Link } from 'react-router-dom';

const useStyles = makeStyles({
  list: {
    width: 250,
  }
});

function LeftDrawer(props) {
  const { open, toggleDrawer } = props;

  const classes = useStyles();

  const iOS = process.browser && /iPad|iPhone|iPod/.test(navigator.userAgent);

  const list = () => (
    <div
      className={classes.list}
      role="presentation"
      onClick={toggleDrawer}
      onKeyDown={toggleDrawer}
    >
      <List>
        <ListItem button component={Link} to="/">
          <ListItemIcon>
            <DirectionsBusIcon />
          </ListItemIcon>
          <ListItemText primary="Planner" />
        </ListItem>
        <ListItem button component={Link} to="/saved">
          <ListItemIcon>
            <BookmarksIcon />
          </ListItemIcon>
          <ListItemText primary="Saved" />
        </ListItem>
      </List>
      <Divider />
    </div>
  );

  return (
      <React.Fragment>
        <SwipeableDrawer
          anchor={'left'}
          open={open}
          onClose={toggleDrawer}
          onOpen={toggleDrawer}
          disableBackdropTransition={!iOS}
          disableDiscovery={iOS}
        >
          {list()}
        </SwipeableDrawer>
      </React.Fragment>
  );
}

const mapStateToProps = createStructuredSelector({
  open: selectDrawerOpen
});

const mapDispatchToProps = dispatch => ({
  toggleDrawer: () => dispatch(toggleDrawer())
});

export default connect(mapStateToProps, mapDispatchToProps)(LeftDrawer);