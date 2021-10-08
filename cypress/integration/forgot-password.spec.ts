import { recurse } from 'cypress-recurse';
import { ForgotPasswordPage } from '../support/pages/forgot-password-page';
import { forceNetworkError, forceServerError } from '../support/utils';

describe('Forgot password page', () => {
  beforeEach(() => {
    ForgotPasswordPage.visit();
  });

  it('should show an error if the form is submitted without input', () => {
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasMissingUsernameOrEmailError();
  });

  it('should show an error if a username or email address is input and then deleted again', () => {
    ForgotPasswordPage.typeUsernameOrEmail('someone');
    ForgotPasswordPage.clearUsernameOrEmail();
    ForgotPasswordPage.hasMissingUsernameOrEmailError();
  });

  it('should show an error if there is a network error', () => {
    forceNetworkError();
    ForgotPasswordPage.typeUsernameOrEmail('someone@example.com');
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasGenericError();
  });

  it('should show an error if there is a server error', () => {
    forceServerError();
    ForgotPasswordPage.typeUsernameOrEmail('someone@example.com');
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasGenericError();
  });

  it('should show an error if a non-existing username or email address is submitted', () => {
    ForgotPasswordPage.typeUsernameOrEmail('unknown-user');
    ForgotPasswordPage.submit();
    ForgotPasswordPage.hasUnknownUsernameOrEmailError();
  });

  it('should display a confirmation message', () => {
    const USERNAME = 'hettlage';
    ForgotPasswordPage.typeUsernameOrEmail(USERNAME);
    ForgotPasswordPage.submit();
    cy.contains(/has been sent/i).should('exist');
  });

  it('should have the input field prepopulated when an email is requested again', () => {
    const USERNAME = 'hettlage';
    ForgotPasswordPage.typeUsernameOrEmail(USERNAME);
    ForgotPasswordPage.submit();

    ForgotPasswordPage.requestAgain();
    ForgotPasswordPage.hasUsernameOrEmail(USERNAME);
  });

  it('should send an email with the correct password reset link', () => {
    // When I request a password reset email
    const USERNAME = 'hettlage';
    ForgotPasswordPage.typeUsernameOrEmail(USERNAME);
    ForgotPasswordPage.submit();
    recurse(
      () => cy.task('getEmailInbox', 'hettlage@saao.ac.za'),
      (emails: Array<any>) => {
        // A boolean (not just a truthy value) must be returned
        return !!emails.length;
      },
      { log: false, delay: 1000, timeout: 20000 }
    ).as('emails');

    // Then one email is sent
    cy.get('@emails').should('have.length', 1);

    // And it is sent to the correct email address
    cy.task('getEmailAddress', USERNAME).then((emailAddress: string) => {
      cy.get('@emails').then((emails: any) => {
        expect(emails[0].to).to.contain(emailAddress);
      });
    });

    // And the email contains a link both in plain text and in html
    cy.get('@emails')
      .then((emails: any) => {
        const LINK_REGEX = /\bhttps?:\/\/[^\s"]+/;
        const email = emails[0];
        const linkInBody = LINK_REGEX.exec(email.body)[0];
        const linkInHtml = LINK_REGEX.exec(email.html)[0];
        expect(linkInBody).to.equal(linkInHtml);

        return linkInBody;
      })
      .then((link: string) => {
        // And when I click on the link I get to the password reset page
        cy.visit(link);
        cy.url().should('contain', 'password-reset');
        // TODO: Continue with the test on the password reset page
      });
  });
});
