# Created by Sapthagiri at 23/03/20
Feature: Assign default tenant(Qwil) to Managers, Platform and Contractor


  Scenario: Check Manager is assigned with the default QWIL tenant
    Given I create a new User
    And I make the created User as Demo Manager
    Then the created Manager should be assigned with default tenant

  Scenario: Check the created User is assigned with the default Qwil tenant
    Given I create a new User
    Then I login to Qwil admin and check the user is assigned with default tenant

  Scenario:Check platform created under the manager(tenant) should be assigned with default tenant(QWIL)
    Given I create a new User
    And I make the created User as Demo Manager
    And I check created Manager is assigned with default tenant
    And I create a platform
    And I activate the platform
    Then the created platform should be assigned with default tenant

  Scenario: Check the platform should have the same tenant as that of the Manager
    Given I create a new user through Qwil admin
    And I create a Manager
    And I make the created Manager as tenant
    And I create a platform
    Then the created platform should be assigned with default tenant