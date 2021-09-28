Cypress.Commands.add('forceNetworkError', () => {
  cy.intercept('/**', { forceNetworkError: true });
});

Cypress.Commands.add('forceServerError', () => {
  cy.intercept('/**', {
    statusCode: 500,
    body: { detail: 'This is a server error' },
  });
});
