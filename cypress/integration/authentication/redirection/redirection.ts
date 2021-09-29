import { Given, Then, When } from 'cypress-cucumber-preprocessor/steps';
import { getUserPassword, updateUserPassword } from '../../utils';
import { LOGIN_URL, LoginPage } from '../../pages/login-page';

const USERNAME = 'hettlage';

const PROPOSAL_CODE = '2020-2-DDT-002';
const PROPOSAL_PAGE_URL = `proposal/${PROPOSAL_CODE}`;

Given('I change the user password', () => {
  updateUserPassword(USERNAME);
});

Given('I go to a proposal page', () => {
  cy.visit(PROPOSAL_PAGE_URL);
});

Given('I am redirected to the login page', () => {
  cy.url().should('contain', LOGIN_URL);
});

When('I login', () => {
  LoginPage.typeUsername(USERNAME);
  LoginPage.typePassword(getUserPassword(USERNAME));
  LoginPage.submit();
});

Then('I am redirected to the proposal page', () => {
  cy.url().should('contain', PROPOSAL_PAGE_URL);
  cy.contains(PROPOSAL_CODE).should('exist');
});
