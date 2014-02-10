# vim: tabstop=4 expandtab shiftwidth=2 softtabstop=2
Feature: Configurable notifications
  As a lone programmer
  I want notification settings to be extracted from code
  So that I could easily change them to suit my needs

  Scenario: Default schedule
    Given the service is running
     Then notification schedule is:
      | message | interval |
      | Ping    | 300      |
