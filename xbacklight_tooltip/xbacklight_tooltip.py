#!usr/bin/env python3

import subprocess
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class app(Gtk.Window):
    '''Hi'''
    def __init__(self, brightness_mod):
        super().__init__()

        self.brightness_mod = brightness_mod
        self.current_brightness = self.poll_brightness()
        self.set_size_request(250, 40)

        self.set_resizable(False)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        label = Gtk.Label("XBL")

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_fraction(self.current_brightness)

        self.add(self.vbox)
        self.vbox.pack_start(label, True, True, 0)
        self.vbox.pack_start(self.progressbar, True, True, 0)

        self.timeout_lifespan = GObject.timeout_add(500, self.on_timeout, None)
        self.timeout_show_mod = GObject.timeout_add(100, self.modify_brightness, None)

    def poll_brightness(self):
        xblight_task = subprocess.Popen('xbacklight', stdout=subprocess.PIPE)
        xblight_task.wait()
        return int(float(xblight_task.communicate()[0].decode('utf-8').strip())) / 100

    def modify_brightness(self, _):
        amount = '10'
        if self.brightness_mod == '-u':
            direction = '-inc'
            brightness_adjust = 0.1
        else:
            direction = '-dec'
            if self.current_brightness > 0.1:
                brightness_adjust = (-0.1)
            else:
                brightness_adjust = 0
                amount = '0'
        xblight_task = subprocess.Popen(['xbacklight', direction, amount], stdout=subprocess.PIPE)
        xblight_task.wait()
        self.progressbar.set_fraction(self.progressbar.get_fraction() + brightness_adjust)

    def on_timeout(self, _):
        '''Bye'''
        Gtk.main_quit()


def main(argv):
    try:
        assert(argv in ('-u', '-d'))
    except AssertionError:
        raise ValueError('Bad command line argument: {}'.format(argv))

    win = app(argv)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main(sys.argv[1])
