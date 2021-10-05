import { ForgotPasswordPage } from './pages/forgot-password-page';
import { forceNetworkError, forceServerError } from './utils';

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

  it.skip('should send an email with the correct password reset link', () => {});
});
