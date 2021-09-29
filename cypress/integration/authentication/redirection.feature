Feature: Redirection after logging in

  Scenario: I'm redirected to a proposal page after logging in

    Given I change the user password
    And I go to a proposal page
    And I am redirected to the login page
    When I login
    Then I am redirected to the proposal page
