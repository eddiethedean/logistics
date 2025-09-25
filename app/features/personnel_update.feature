Feature: Personnel Class Update
  As a user
  I want to update personnel class information
  So that I can maintain accurate personnel records

  Scenario: A user updates a personnel class
    Given a UI exists with forms
    When a user saves content to personnel
    Then new content is saved to database
