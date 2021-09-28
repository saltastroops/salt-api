Feature: Logging in

  Background:
    Given I am on the login page

  Scenario: I try to login with no username

    When I enter the password "secret"
    And I submit the form
    Then I get a username error

  Scenario: I enter a username and remove it again

    When I enter the username "secret"
    And I remove the username
    Then I get a username error

  Scenario: I try to login with no password

    When I enter the username "someone"
    And I submit the form
    Then I get a password error

  Scenario: I enter a password and remove it again

    When I enter the password "secret"
    And I remove the password
    Then I get a password error
