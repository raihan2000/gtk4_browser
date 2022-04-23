#!/usr/bin/env python

import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit2', '5.0')
from gi.repository import Gtk, Adw, WebKit2, GLib, Gio

app_title = "Browser"
app_id = "com.github.raihan2000.browser"

class MyApp(Adw.Application):
  def __init__(self):
      self.app = Adw.Application(application_id=app_id)
      self.app.connect('activate', self.on_activate)

      GLib.set_application_name(app_title)

  def on_activate(self, app):
      self.win = Gtk.ApplicationWindow(application=app)

      self.header = Gtk.HeaderBar()
      self.win.set_titlebar(self.header)

      self.search = Gtk.SearchEntry()

      self.search.connect("activate", self.on_search)

      #Menu
      self.action = Gio.SimpleAction.new("something", None)
      self.action.connect("activate", self.print_something)
      self.win.add_action(self.action)

      #Menu
      menu = Gio.Menu.new()
      menu.append("Do Something", "win.something")

      #popover
      self.popover = Gtk.PopoverMenu()
      self.popover.set_menu_model(menu)

      self.ham = Gtk.MenuButton()
      self.ham.set_popover(self.popover)
      self.ham.set_icon_name("open-menu-symbolic")

      self.header.pack_end(self.ham)
      self.header.pack_start(self.search)

      self.web = WebKit2.WebView()
      self.web.load_uri("https://duckduckgo.com")
      self.web.connect('notify::estimated-load-progress', self.change_url)
      self.win.set_child(self.web)
      self.win.present()

  def run(self):
      self.app.run(None)

  def on_search(self, add):
      add = self.search.get_text()
      if add.startswith("https://") or add.startswith("http://"):
          self.web.load_uri(add)
      else:
          add = "https://" + add
          self.web.load_uri(add)

  def print_something(self, action, param):
      print("somthing")

  def change_url(self, widget, frame):
      uri = self.web.get_uri()
      self.search.set_text(uri)

app = MyApp()
app.run()
