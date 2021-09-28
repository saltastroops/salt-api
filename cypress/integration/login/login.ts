import { Given, Then, When } from 'cypress-cucumber-preprocessor/steps';
import { LoginPage } from '../../pages/login-page';

Given(/^I am on the login page$/, () => {
  LoginPage.visit();
});

When(/^I enter a valid username$/, function () {
  LoginPage.typeUsername('someone');
});

When(/^I submit the form$/, () => {
  LoginPage.submit();
});

Then(/^I get an error$/, () => {
  cy.get("[data-test='error']")
    .contains(/password/i)
    .should('exist');
});
