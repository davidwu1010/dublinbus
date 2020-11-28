describe('The home page', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('Shows a basic UI', () => {
    cy.title().should('equal', 'Dublin Bus'); // title
    cy.contains('Dublin Bus');  // logo
    cy.contains('Sign In'); // sign in button
    cy.contains('By Stops'); // trip planner tab1
    cy.contains('By Places'); // trip planner tab2
  });

  it('Is responsive', () => {
    cy.viewport(1920, 1080);
    cy.get('.gm-style').should('exist'); // display google maps
    cy.viewport('iphone-x');
    cy.get('.gm-style').should('not.exist');  // hide google maps
  });
})