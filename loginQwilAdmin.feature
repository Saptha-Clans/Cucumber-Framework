# Created by Sapthagiri at 24/02/20

Feature: Qwil admin action

  Background:
    Given I am in the Qwil admin webpage
    When I enter the user email and password and login

  @slow
  Scenario: Create contractor under a platform
    And I visit the user detail page and create a user
    And I make the created user as Manager and assign tenant
    And I create a platform under the Manager
    And I add Contractor to the Platform
    And I logout the Qwil admin
    Then I was able to successfully add a contractor under a platform

  @slow
  Scenario: Create a Contractor under a tenant Manager
    And I visit the user detail page and create a user
    And I make the created user as Manager and assign tenant
    And I add Contractor to the under a Manager
    And I logout the Qwil admin
    Then I was able to successfully add a contractor under a Manager