import { Given, Then, When } from 'cypress-cucumber-preprocessor/steps';
import { LOGIN_URL, LoginPage } from '../../pages/login-page';
import { getUserPassword, updateUserPassword } from '../../utils';

const USERNAME = 'hettlage';

Given('I am on the login page', () => {
  LoginPage.visit();
});

Given('I change the user password', () => {
  updateUserPassword(USERNAME);
});

When('I enter the username {string}', (username) => {
  LoginPage.typeUsername(username);
});

When('I remove the username', () => {
  LoginPage.clearUsername();
});

When('I enter the password {string}', (password) => {
  LoginPage.typePassword(password);
});

When('I get a username error', () => {
  LoginPage.hasUsernameError();
});

When('I remove the password', () => {
  LoginPage.clearPassword();
});

When('I get a password error', () => {
  LoginPage.hasPasswordError();
});

When('I enter the username and password', () => {
  LoginPage.typeUsername(USERNAME);
  LoginPage.typePassword(getUserPassword(USERNAME));
});

When('I enter the username and a wrong password', () => {
  LoginPage.typeUsername(USERNAME);
  LoginPage.typePassword('incorrect');
});

When('I submit the form', () => {
  LoginPage.submit();
});

Then('another page is loaded', () => {
  cy.url().should('not.contain', LOGIN_URL);
});

Then('I get a generic error', () => {
  LoginPage.hasGenericError();
});

Then('I get a username or password error', () => {
  LoginPage.hasUsernameOrPasswordError();
});
