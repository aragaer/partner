# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from datetime import timedelta
from unittest.mock import DEFAULT, MagicMock, Mock, patch

from partner import PartnerService


@given('the service is running')
def step_impl(context):
    kwargs = context.service_kwargs if 'service_kwargs' in context else {}
    context.service = PartnerService(**kwargs)


@when('it is time to show notification')
def step_impl(context):
    interval = context.scheduler.get_timeout_for(
        lambda event: event.callback == context.service.show_notification)
    assert interval is not None
    context.scheduler.advance_time(interval)


@then('notification appears')
def step_impl(context):
    assert context.notification.called
    assert context.notification.return_value.show.called


@then('notification did not appear')
def step_impl(context):
    assert not context.notification.return_value.show.called


@given('the notification should appear every {minutes:d} minutes')
def step_impl(context, minutes):
    context.scheduler.events = []
    context.service.period = minutes * 60


@given('notification appears')
def step_impl(context):
    context.service.show_notification("Notify")
    context.notification.return_value.show.reset_mock()


@when('{time} pass')
def step_impl(context, time):
    components = time.split()
    delta = timedelta(**dict(
        (c, int(t)) for c, t in zip(components[1::2], components[::2])))
    context.scheduler.advance_time(delta.total_seconds())


@then('notification will appear in {time}')
def step_impl(context, time):
    interval = context.scheduler.get_timeout_for(
        lambda event: event.callback == context.service.show_notification)
    assert interval is not None
    allow_less = time.startswith('less than')
    if allow_less:
        time = time[10:]
    components = time.split()
    delta = timedelta(**dict(
        (c, int(t)) for c, t in zip(components[1::2], components[::2])))
    timeout = delta.total_seconds()
    if allow_less:
        assert interval <= timeout
    else:
        assert interval == timeout


@when('I start the main application')
def step_impl(context):
    def intercept_service(*args, **kwargs):
        context.service = PartnerService(*args, **kwargs)
        return context.service

    with patch('partner.PartnerService', new=intercept_service):
        from start import main

        main()


@then('the service is started')
def step_impl(context):
    assert context.service is not None


@then('a greeting notification is shown once')
def step_impl(context):
    context.execute_steps('''
        Then 'Hello' message is shown once
    ''')


@then('notification is closed')
def step_impl(context):
    assert context.notification.return_value.close.called


@then('notification schedule is')
def step_impl(context):
    schedule = dict((row['message'], int(row['interval']))
                    for row in context.table)
    assert schedule.items() == context.service.schedule.items()


@given('the notification schedule is')
def step_impl(context):
    schedule = dict((row['message'], int(row['interval']))
                    for row in context.table)
    context.service_kwargs = {'schedule': schedule}


@then('\'{message}\' message is shown once')
def step_impl(context, message):
    context.notification.assert_called_once_with(message, None, None)
    context.notification.return_value.show.assert_called_once_with()
    context.notification.reset_mock()
    context.notification.return_value.show.reset_mock()
