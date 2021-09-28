import { Given, Then, When } from 'cypress-cucumber-preprocessor/steps';
import { LoginPage } from '../pages/login-page';

Given(/^I am on the login page$/, () => {
  LoginPage.visit();
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

When('I submit the form', () => {
  LoginPage.submit();
});
