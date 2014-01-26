#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

from partner import PartnerService


def main():
    """
        Entry point.
    """

    DBusGMainLoop(set_as_default=True)
    PartnerService()
    GObject.MainLoop().run()


if __name__ == '__main__':
    main()
