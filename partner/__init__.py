#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import dbus
from gi.repository import GLib


class PartnerService(object):
    """
        Main service for the class.
    """

    period = 300
    _delay = 1
    schedule = {'Ping': 300}

    def __init__(self, notifier=None, scheduler=None):
        if notifier is None:
            notifier = NotifyNotifier()
        self.notifier = notifier
        if scheduler is None:
            scheduler = GLibScheduler()
        self.scheduler = scheduler
        self.scheduler.schedule_at(300, self.show_notification, "Ping")
        self.notifier.show_notification("Hello")

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        """
            Set the delay to next notification.
        """
        if value == 0:
            value = self.period
            self.show_notification()
        self._delay = value

    def show_notification(self, message):
        """
            Say something to the lone developer.
        """
        self.notifier.show_notification(message)
        self.scheduler.schedule_at(self.period,
                                   self.show_notification,
                                   message)


class NotifyNotifier(object):
    """
        Uses gi.repository to show notifications.
    """

    def __init__(self):
        from gi.repository.Notify import init
        init("Partner")

    def show_notification(self, message, timeout=10):
        """
            Show notification.
        """
        from gi.repository.Notify import Notification

        n = Notification.new(message, None, None)
        n.set_timeout(timeout * 1000)
        n.show()


class GLibScheduler(object):
    """
        Used for stting up deferred jobs.
    """

    def schedule_at(self, delay, callback, *args):
        """
            Schedule a function at a given delay.
        """
        GLib.timeout_add_seconds(delay, callback, *args)
