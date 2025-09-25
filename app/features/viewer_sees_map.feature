Feature: Viewer sees map
  As a viewer
  I want to see the LogCOP map
  So that I can view tactical logistics information geographically

  Scenario: Viewer accesses the map
    Given a viewer wants to see the LogCOP
    When a user accesses the application
    Then they see a map
