import '@testing-library/cypress/add-commands';

describe('App', () => {
  it('Can sign in and sign out', () => {
    cy.visit('/sign-in');
    cy.findByLabelText(/Email Address/i).type('test@test.com');  // enter email
    cy.findByLabelText(/Password/i).type('qwerty');  // enter password
    cy.get('[type="submit"]').click();  // sign in
    cy.contains(/sign out/i);  // sign in succeeded
    cy.get('.MuiToolbar-root > .MuiButton-root').click();  // sign out
    cy.contains(/sign in/i);  // sign out succeeded
  });
});