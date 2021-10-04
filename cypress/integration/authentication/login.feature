Feature: Logging in

  Background:
    Given I go to the login page

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

  Scenario: Logging in with a server error

    Given I change the user password
    And there is a server error
    When I enter the username and password
    And I submit the form
    Then I get a generic error

  Scenario: Logging in with a network failure

    Given I change the user password
    And there is a network error
    When I enter the username and password
    And I submit the form
    Then I get a generic error

  Scenario: Trying to login with incoprrect credentials

    When I enter the username and a wrong password
    And I submit the form
    Then I get a username or password error

  Scenario: I login

    Given I change the user password
    When I enter the username and password
    And I submit the form
    Then another page is loaded

  Scenario: I try to login even though I'm logged in already

    Given I am logged in
    When I go to the login page
    Then another page is loaded
