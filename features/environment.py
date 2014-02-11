#!/usr/bin/python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from types import SimpleNamespace
from unittest.mock import DEFAULT, MagicMock, Mock, patch


class MockScheduler(object):

    def __init__(self):
        self.events = []

    def schedule_at(self, interval, callback, *args, **kwargs):
        position = 0
        for event in self.events:
            if interval > event.delay:
                interval -= event.delay
                position += 1
            else:
                event.delay -= interval
                break

        self.events.insert(position,
            SimpleNamespace(delay=interval, callback=callback, args=args,
                            kwargs=kwargs))

    def advance_time(self, change):
        while self.events:
            event = self.events[0]
            if event.delay > change:
                event.delay -= change
                return
            change -= event.delay
            self.events.pop(0)
            event.callback(*event.args, **event.kwargs)

    def get_timeout_for(self, filter_func):
        timeout = 0
        for event in self.events:
            timeout += event.delay
            if filter_func(event):
                return timeout


def before_all(context):
    context.global_patchers = []

    patcher = patch('gi.repository.GObject.MainLoop')
    context.global_patchers.append(patcher)
    context.mock_loop = patcher.start()

    context.mock_run = Mock()
    context.mock_loop.return_value.run = context.mock_run

    patcher = patch('dbus.mainloop.glib.DBusGMainLoop')
    context.global_patchers.append(patcher)
    context.mock_mainloop = patcher.start()

    context.scheduler = MockScheduler()

    patcher = patch('gi.repository.GLib.timeout_add_seconds',
                    new=context.scheduler.schedule_at)
    context.global_patchers.append(patcher)
    patcher.start()

    patcher = patch('gi.repository.Notify.Notification.new')
    context.global_patchers.append(patcher)
    context.notification = patcher.start()

    def schedule_close():
        mock_notification = context.notification.return_value
        mock_set_timeout = mock_notification.set_timeout
        if mock_set_timeout.called:
            ms = mock_set_timeout.call_args[0][0]
            context.scheduler.schedule_at(ms/1000, mock_notification.close)
        return DEFAULT

    context.notification.return_value.show.side_effect = schedule_close


def after_all(context):
    for patcher in context.global_patchers:
        patcher.stop()


def after_scenario(context, scenario):
    for mock in [context.notification,
                 context.notification.return_value.show]:
        mock.reset_mock()

    context.scheduler.events = []
