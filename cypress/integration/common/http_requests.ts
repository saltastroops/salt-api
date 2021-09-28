import { Given } from 'cypress-cucumber-preprocessor/steps';

Given('there is a server error', () => {
  cy.forceServerError();
});

Given('there is a network error', () => {
  cy.forceNetworkError();
});
