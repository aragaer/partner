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

  @wip
  Scenario Outline: Custom message/interval
    Given the notification schedule is:
        | message   | interval   |
        | <message> | <interval> |
      And the service is running
     Then notification will appear in less than <interval> seconds
     When <interval> seconds pass
     Then '<message>' message is shown

    Examples: Custom message:
      | message     | interval  |
      | Howdy       | 300       |
      | Missed me?  | 300       |

    Examples: Custom interval:
      | message     | interval  |
      | Ping        | 180       |
      | Ping        | 240       |
      | Ping        | 750       |

    Examples: Custom both:
      | message         | interval  |
      | Howdy           | 350       |
      | Go get some tea | 600       |
