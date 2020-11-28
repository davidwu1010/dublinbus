import React from 'react';
import Card from '@material-ui/core/Card';
import Typography from '@material-ui/core/Typography';
import CardActionArea from '@material-ui/core/CardActionArea';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  pContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center'
  },
  p: {
    width: '340px'
  }
});

function RouteCard(props) {
  const { steps, clickHandler } = props;

  const classes = useStyles();

  function stepToDescription(step) {
    let instructions = step.instructions;
    if (step.travel_mode === 'TRANSIT') {
      instructions += ', Bus ' + step.transit.line.short_name;
    }

    instructions += ', ' + step.duration.text;
    return instructions;
  }

  return (
    <Card variant="outlined">
      <CardActionArea onClick={clickHandler}>
        <div className={classes.pContainer}>
        { steps.map((step, index) => (<Typography variant="body1" key={index} className={classes.p}>{stepToDescription(step)}</Typography>)) }
        </div>
      </CardActionArea>
    </Card>
  );
}


export default RouteCard;