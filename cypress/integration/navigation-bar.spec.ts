import { HomePage } from '../support/pages/home-page';
import {
  forceNetworkError,
  forceServerError,
  interceptIndefinitely,
} from '../support/utils';
import { User } from '../support/types';
import { NavigationBar } from '../support/components/navigation-bar';

const USERNAME = 'hettlage';

describe('Inline login form', () => {
  beforeEach(() => {
    // Ensure the inline login form is not hidden because of a small screen size
    cy.viewport(1500, 2000);
  });

  it('should give an error if the username is missing', () => {
    HomePage.visit();
    NavigationBar.typePassword('secret');
    NavigationBar.submitLogin();
    NavigationBar.hasUsernameError();
  });

  it('should give an error if the username is missing', () => {
    HomePage.visit();
    NavigationBar.typeUsername('someone');
    NavigationBar.submitLogin();
    NavigationBar.hasPasswordError();
  });

  it('should give an error if there is a network error', () => {
    HomePage.visit();
    forceNetworkError();
    NavigationBar.typeUsername('someone');
    NavigationBar.typePassword('secret');
    NavigationBar.submitLogin();
    NavigationBar.hasGenericLoginError();
  });

  it('should give an error if there is a server error', () => {
    HomePage.visit();
    forceServerError();
    NavigationBar.typeUsername('someone');
    NavigationBar.typePassword('secret');
    NavigationBar.submitLogin();
    NavigationBar.hasGenericLoginError();
  });

  it('should give an error if the username or password is incorrect', () => {
    cy.task('updateUserPassword');
    NavigationBar.typeUsername(USERNAME);
    NavigationBar.typePassword('secret');
    NavigationBar.submitLogin();
    NavigationBar.hasUsernameOrPasswordError();
  });

  it('should log the user in if the username and password are valid', () => {
    cy.task('updateUserPassword', USERNAME).then((password: string) => {
      cy.task('getUser', USERNAME).then((user: User) => {
        HomePage.visit();
        NavigationBar.typeUsername(USERNAME);
        NavigationBar.typePassword(password);
        NavigationBar.submitLogin();
        NavigationBar.hasNoLoginForm();
        NavigationBar.hasWelcomeMessage(user.givenName);
      });
    });
  });

  it('should indicate a loading state until a successful login request finishes', () => {
    cy.task('updateUserPassword', USERNAME).then((password: string) => {
      const interception = interceptIndefinitely('token');
      HomePage.visit();
      NavigationBar.typeUsername(USERNAME);
      NavigationBar.typePassword(password);
      NavigationBar.submitLogin();
      NavigationBar.loginIsLoading().then(() => {
        interception.sendResponse();
        NavigationBar.loginIsNotLoading();
      });
    });
  });

  it('should indicate a loading state until an unsuccessful login request finishes', () => {
    cy.task('updateUserPassword', USERNAME).then((password: string) => {
      const interception = interceptIndefinitely('token');
      HomePage.visit();
      NavigationBar.typeUsername(USERNAME);
      NavigationBar.typePassword('incorrect');
      NavigationBar.submitLogin();
      NavigationBar.loginIsLoading().then(() => {
        interception.sendResponse();
        NavigationBar.loginIsNotLoading();
      });
    });
  });
});
