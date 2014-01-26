#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from unittest import TestCase
from unittest.mock import Mock, patch

from partner import GLibScheduler


class GLibSchedulerTest(TestCase):

    @patch('gi.repository.GLib.timeout_add_seconds')
    def test_add_timeout_should_use_gobject(self, mock_add):
        def callback():
            pass
        scheduler = GLibScheduler()
        scheduler.schedule_at(1000, callback)

        mock_add.assert_called_once_with(1000, callback)

    @patch('gi.repository.GLib.timeout_add_seconds')
    def test_should_pass_whatever_args(self, mock_add):
        def callback(*args):
            pass
        scheduler = GLibScheduler()
        for args in [[], [1, 2, 3], [[]]]:
            mock_add.reset_mock()

            scheduler.schedule_at(1000, callback, *args)

            mock_add.assert_called_once_with(1000, callback, *args)
