Feature: Supply Class Update
  As a logistician
  I want to update supply class information
  So that I can maintain accurate supply records

  Scenario: Logistician updates a supply class
    Given an UI exists
    When a user saves content to supply form
    Then new content is saved to supply database
