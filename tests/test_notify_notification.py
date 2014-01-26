#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from unittest import TestCase
from unittest.mock import Mock, patch

from partner import NotifyNotifier


class NotifierConstructorTest(TestCase):

    @patch('gi.repository.Notify.init')
    def test_should_init_dbus(self, mock_init):
        NotifyNotifier()

        mock_init.assert_called_with('Partner')


class NotifierShowNotificationTest(TestCase):

    @patch('gi.repository.Notify.Notification.new')
    def test_should_show_desktop_notification(self, mock_new):
        notifier = NotifyNotifier()
        notifier.show_notification("Message")

        mock_new.assert_called_once_with("Message", None, None)
        self.assertTrue(mock_new.return_value.show.called)

    @patch('gi.repository.Notify.Notification.new')
    def test_should_set_timeout_passed_in_seconds(self, mock_new):
        notifier = NotifyNotifier()
        notifier.show_notification("Message", timeout=5)

        mock_new.return_value.set_timeout.assert_called_once_with(5000)

    @patch('gi.repository.Notify.Notification.new')
    def test_should_set_timeout_to_10_seconds(self, mock_new):
        notifier = NotifyNotifier()
        notifier.show_notification("Message")

        mock_new.return_value.set_timeout.assert_called_once_with(10000)
