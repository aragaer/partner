# vim: tabstop=4 expandtab shiftwidth=2 softtabstop=2
Feature: Notification
  As a solo developer
  I want a regular notification to appear
  So that I could switch between tasks instead of staying on one task for too
  long

  Background: The partner is active
    Given the service is running

  Scenario: Notification
     When it is time to show notification
     Then notification appears

  Scenario: Regular notifications
    Given the notification should appear every 5 minutes
      And notification appears
     Then notification will appear in 5 minutes
     When 5 minutes pass
     Then notification appears

  Scenario: Not too often
    Given the notification should appear every 10 minutes
      And notification appears
     When 3 minutes pass
     Then notification did not appear
      And notification will appear in 7 minutes

  Scenario: Notification timeout
    Given notification appears
     When 30 seconds pass
     Then notification is closed
