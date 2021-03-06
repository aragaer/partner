#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from gi.repository import GLib


class PartnerService(object):
    """
        Main service for the class.
    """

    schedule = {'Ping': 300}

    def __init__(self, notifier=None, scheduler=None, schedule=None):
        if notifier is None:
            notifier = NotifyNotifier()
        self.notifier = notifier
        if scheduler is None:
            scheduler = GLibScheduler()
        if schedule is not None:
            self.schedule = schedule
        self.scheduler = scheduler
        for message, interval in self.schedule.items():
            self.scheduler.schedule_at(interval, self.show_notification, message)
        self.notifier.show_notification("Hello")

    def show_notification(self, message):
        """
            Say something to the lone developer.
        """
        self.notifier.show_notification(message)
        if message in self.schedule:
            self.scheduler.schedule_at(self.schedule[message],
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
