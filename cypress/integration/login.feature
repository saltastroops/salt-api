Feature: Logging in

  Scenario: I try to login with no username

    Given I am on the login page
    When I enter a valid username
    And I submit the form
    Then I get an error
