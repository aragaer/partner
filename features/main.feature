# vim: tabstop=4 expandtab shiftwidth=2 softtabstop=2
Feature: Running the application
  As a developer
  I want to be able to start the service
  So that I would get me a virtual partner

  Scenario: Running the main
     When I start the main application
     Then the service is started
      And notification will appear in less than 5 minutes

  Scenario: Greeting
     When I start the main application
     Then a greeting notification is shown once
