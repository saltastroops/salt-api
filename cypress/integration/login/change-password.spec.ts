import {
  forceNetworkError,
  forceServerError,
  interceptIndefinitely,
} from '../../support/utils';
import { ChangePasswordPage } from '../../support/pages/login/change-password-page';

describe('Change password page', () => {
  it('should show an error if the form is submitted without any input', () => {
    ChangePasswordPage.visit('some-token');
    ChangePasswordPage.submit();
    ChangePasswordPage.hasMissingNewPasswordError();
    ChangePasswordPage.hasMissingRetypedNewPassword();
  });

  it('should show an error if only new password input has text', () => {
    ChangePasswordPage.visit('some-token');
    const newPassword = 'new-password';
    ChangePasswordPage.typeNewPassword(newPassword);
    ChangePasswordPage.submit();
    ChangePasswordPage.hasNewPassword(newPassword);
    ChangePasswordPage.hasMissingRetypedNewPassword();
  });
  it('should show an error if only new password again input has text', () => {
    ChangePasswordPage.visit('some-token');
    const newRePassword = 'new-password';
    ChangePasswordPage.typeRetypedNewPassword(newRePassword);
    ChangePasswordPage.submit();
    ChangePasswordPage.hasRetypedNewPassword(newRePassword);
    ChangePasswordPage.hasMissingNewPasswordError();
  });

  it('should show an error if a password is input and then deleted again', () => {
    ChangePasswordPage.visit('some-token');
    ChangePasswordPage.submit();
    ChangePasswordPage.typeNewPassword('new-password');
    ChangePasswordPage.clearNewPassword();
    ChangePasswordPage.hasMissingNewPasswordError();
  });

  it('should show an error if a retyped password is input and then deleted again', () => {
    ChangePasswordPage.visit('some-token');
    ChangePasswordPage.submit();
    ChangePasswordPage.typeRetypedNewPassword('new-password');
    ChangePasswordPage.clearRetypedNewPassword();
    ChangePasswordPage.hasMissingRetypedNewPassword();
  });

  it('should show an error if the password and retyped password are not the same', () => {
    ChangePasswordPage.visit('some-token');
    ChangePasswordPage.typeNewPassword('new-password');
    ChangePasswordPage.typeRetypedNewPassword('different-new-password');
    ChangePasswordPage.submit();
    ChangePasswordPage.hasPasswordMismatchError();
  });

  it('should show an error if there is a network error', () => {
    ChangePasswordPage.visit('some-token');
    const newPassword = 'new-password';
    forceNetworkError();
    ChangePasswordPage.typeNewPassword(newPassword);
    ChangePasswordPage.typeRetypedNewPassword(newPassword);
    ChangePasswordPage.submit();
    ChangePasswordPage.hasGenericError();
  });

  it('should show an error if there is a server error', () => {
    ChangePasswordPage.visit('some-token');
    const newPassword = 'new-password';
    forceServerError();
    ChangePasswordPage.typeNewPassword(newPassword);
    ChangePasswordPage.typeRetypedNewPassword(newPassword);
    ChangePasswordPage.submit();
    ChangePasswordPage.hasGenericError();
  });

  it('should show a meaningful error if the password is changed with an invalid token', () => {
    ChangePasswordPage.visit('invalid-token');
    ChangePasswordPage.changePassword('new-password');

    ChangePasswordPage.hasAuthenticationError();
    ChangePasswordPage.isNotLoading();
  });

  it('should show a loading indicator while the password is being changed', () => {
    interceptIndefinitely('user');
    ChangePasswordPage.visit('invalid-token');
    ChangePasswordPage.changePassword('new-password');
    ChangePasswordPage.isLoading();
  });

  // Testing the case of a successful password change is covered by the integration
  // tests for the forgot password page.
});
