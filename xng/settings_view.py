#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  This file is part of solus-sc
#
#  Copyright © 2014-2018 Ikey Doherty <ikey@solus-project.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#

from gi.repository import Gtk, Gio
from . import join_resource_path


class ScSettingsView(Gtk.Box):
    """ Enable controlling the Software Center settings from the sidebar
    """

    __gtype_name__ = "ScSettingsView"

    context = None

    def __init__(self, context):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.context = context

        self.set_border_width(10)

        builder = Gtk.Builder()
        rp = join_resource_path("settings.ui")

        builder.add_from_file(rp)

        # Main view itself
        main_grid = builder.get_object("main_grid")
        main_grid.reparent(self)

        # Check for updates
        self.check_button = builder.get_object("switch_check_updates")

        # Hook up settings
        self.settings = Gio.Settings.new("com.solus-project.software-center")
        self.settings.bind("check-updates",
                           self.check_button, "active",
                           Gio.SettingsBindFlags.DEFAULT)

        # Can do it on metered?
        mbutton = builder.get_object("switch_enable_metered")
        self.settings.bind("update-on-metered",
                           mbutton, "active",
                           Gio.SettingsBindFlags.DEFAULT)

        # Fetch screenies?
        mbutton = builder.get_object("switch_fetch_media")
        self.settings.bind("fetch-media",
                           mbutton, "active",
                           Gio.SettingsBindFlags.DEFAULT)

        # Update frequency
        combo = builder.get_object("combo_frequency")
        model = Gtk.ListStore(str, str)
        # Check for updates every hour
        model.append([_("Every hour"), "hourly"])
        # Check for updates once per day
        model.append([_("Daily"), "daily"])
        # Check for updates once a week
        model.append([_("Weekly"), "weekly"])
        combo.set_id_column(1)
        combo.set_model(model)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)

        # Connect to enum settings
        self.settings.bind("update-frequency",
                           combo, "active-id", Gio.SettingsBindFlags.DEFAULT)

        # Update type
        combo = builder.get_object("combo_type")
        model = Gtk.ListStore(str, str)
        # Notify of all updates
        model.append([_("All updates"), "all"])
        # Notify only of security updates
        model.append([_("Security updates only"), "security-only"])
        # Notify of security and core system updates ("mandatory")
        model.append([_("Security & core updates"), "security-and-mandatory"])
        combo.set_id_column(1)
        combo.set_model(model)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)

        # Connect to enum settings
        self.settings.bind("update-type",
                           combo, "active-id", Gio.SettingsBindFlags.DEFAULT)
