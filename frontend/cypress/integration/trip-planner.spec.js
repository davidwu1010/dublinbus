import '@testing-library/cypress/add-commands';

describe('The trip planner', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('Can estimate travel times', () => {
    cy.findByLabelText(/route/i).type('39a{enter}');  // select route
    cy.findByLabelText(/origin/i).type('767{enter}');  // select origin stop
    cy.findByLabelText(/dest/i).type('2171{enter}');  // select destination stop
    cy.findByText(/submit/i).click();  // submit form
    cy.contains(/^[1-9]?[0-9]* mins$/);  // get travel time prediction
  });
});