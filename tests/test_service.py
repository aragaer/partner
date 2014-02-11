#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from unittest import TestCase, skip
from unittest.mock import Mock, patch

from partner import PartnerService


class ServiceTest(TestCase):

    def test_should_renew_notification_timer(self):
        scheduler = Mock()
        service = PartnerService(scheduler=scheduler, notifier=Mock())
        for period in [300, 600]:
            scheduler.schedule_at.reset_mock()
            service.period = period
            service.show_notification("Something")

            scheduler.schedule_at.assert_called_once_with(period,
                service.show_notification, "Something")

    def test_should_call_notifier(self):
        notifier = Mock()
        service = PartnerService(notifier=notifier, scheduler=Mock())
        for message in ["Stuff", "Something"]:
            notifier.show_notification.reset_mock()

            service.show_notification(message)

            notifier.show_notification.assert_called_once_with(message)

    @patch('partner.NotifyNotifier.show_notification')
    def test_should_use_notifier_by_default(self, mock_show):
        service = PartnerService(scheduler=Mock())

        service.show_notification("Something")

        self.assertTrue(mock_show.called)

    def test_should_schedule_notification_in_constructor(self):
        "Ping notification which will appear somewhere in first 5 minutes."
        scheduler = Mock()
        service = PartnerService(scheduler=scheduler, notifier=Mock())

        self.assertTrue(scheduler.schedule_at.called)
        call_args = scheduler.schedule_at.call_args[0]
        self.assertLessEqual(call_args[0], 300)
        self.assertEqual(call_args[1], service.show_notification)
        self.assertEqual(call_args[2], "Ping")

    @patch('partner.GLibScheduler.schedule_at')
    def test_should_use_glib_scheduler_by_default(self, mock_schedule_at):
        "This test assumes that schedule_at is called in constructor."
        service = PartnerService(notifier=Mock())

        self.assertTrue(mock_schedule_at.called)

    @patch('partner.PartnerService.show_notification')
    def test_should_show_greeting_once_in_constructor(self, mock_show):
        notifier = Mock()
        service = PartnerService(scheduler=Mock(), notifier=notifier)

        notifier.show_notification.assert_called_once_with("Hello")
        self.assertFalse(mock_show.called)

    def test_should_have_5_minutes_default_period(self):
        scheduler=Mock()
        service = PartnerService(notifier=Mock(), scheduler=scheduler)
        scheduler.schedule_at.reset_mock()

        service.show_notification("Message")

        scheduler.schedule_at.assert_called_once_with(300,
            service.show_notification, "Message")

    def test_should_have_default_schedule(self):
        service = PartnerService(notifier=Mock(), scheduler=Mock())

        self.assertEqual(service.schedule.items(), {'Ping': 300}.items())

    def test_should_accept_schedule_in_constructor(self):
        service = PartnerService(notifier=Mock(), scheduler=Mock(),
                                 schedule={'Howdy': 300})

        self.assertEqual(service.schedule.items(), {'Howdy': 300}.items())
