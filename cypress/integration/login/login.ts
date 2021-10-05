import { LOGIN_URL, LoginPage } from '../pages/login-page';
import {
  forceNetworkError,
  forceServerError,
  login,
  updateUserPassword,
} from '../utils';
import { PROPOSAL_BASE_URL, ProposalPage } from '../pages/proposal-page';

const USERNAME = 'hettlage';

describe('Login page', () => {
  beforeEach(() => {
    LoginPage.visit();
  });

  it('should give an error for a missing username', () => {
    LoginPage.typePassword('secret');
    LoginPage.submit();
    LoginPage.hasUsernameError();
  });

  it('should give an error for a missing password', () => {
    LoginPage.typeUsername('someone');
    LoginPage.submit();
    LoginPage.hasPasswordError();
  });

  it('should give an error after the username is removed again', () => {
    LoginPage.typeUsername('someone');
    LoginPage.clearUsername();
    LoginPage.hasUsernameError();
  });

  it('should give an error after the password is removed again', () => {
    LoginPage.typePassword('secret');
    LoginPage.clearPassword();
    LoginPage.hasPasswordError();
  });

  it('should give an error if there is a server error', () => {
    const password = updateUserPassword(USERNAME);
    forceServerError();
    LoginPage.typeUsername(USERNAME);
    LoginPage.typePassword(password);
    LoginPage.submit();
    LoginPage.hasGenericError();
  });

  it('should give an error if there is a network error', () => {
    const password = updateUserPassword(USERNAME);
    forceNetworkError();
    LoginPage.typeUsername(USERNAME);
    LoginPage.typePassword(password);
    LoginPage.submit();
    LoginPage.hasGenericError();
  });

  it('should give an error if you login with an incorrect password', () => {
    LoginPage.typeUsername(USERNAME);
    LoginPage.typePassword('incorrect');
    LoginPage.submit();
    LoginPage.hasUsernameOrPasswordError();
  });

  it('should log you in if you use the correct username and password', () => {
    cy.url().should('contain', LOGIN_URL);
    const password = updateUserPassword(USERNAME);
    LoginPage.typeUsername(USERNAME);
    LoginPage.typePassword(password);
    LoginPage.submit();
    cy.url().should('not.contain', LOGIN_URL);
  });

  it('should redirect to another page if you are logged in already', () => {
    login(USERNAME);
    LoginPage.visit();
    cy.url().should('not.contain', LOGIN_URL);
  });

  it('should take me to the originally requested page after logging in', () => {
    // When I'm not logged in
    // And I go to a proposal page
    // Then I'm redirected to the login page
    // And when I then login
    // Then I'm redirected to the originaly requested proposal page
    ProposalPage.visit('2020-2-SCI-043');
    cy.url().should('not.contain', PROPOSAL_BASE_URL);
    const password = updateUserPassword(USERNAME);
    LoginPage.typeUsername(USERNAME);
    LoginPage.typePassword(password);
    LoginPage.submit();
    cy.url().should('contain', PROPOSAL_BASE_URL);
  });
});
