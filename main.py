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

      ##Create Widgets for Header
      self.tab_btn = Gtk.Button(label="Tab")
      self.refresh_btn = Gtk.Button(label="Refresh")
      self.back_btn = Gtk.Button(label="Back")
      self.forward_btn = Gtk.Button(label="Forward")
      self.search = Gtk.SearchEntry()
      self.info_btn = Gtk.MenuButton()

      ##Add Header
      self.header = Gtk.HeaderBar()
      self.win.set_titlebar(self.header)

      ##Info Menu
      self.action = Gio.SimpleAction.new("something", None)
      self.win.add_action(self.action)
      menu = Gio.Menu.new()
      menu.append("Do Something", "win.something")
      self.popover = Gtk.PopoverMenu()
      self.popover.set_menu_model(menu)
      self.info_btn.set_popover(self.popover)

      ##Set Icons of Widgets
      self.tab_btn.set_icon_name("tab-new-symbolic")
      self.info_btn.set_icon_name("open-menu-symbolic")
      self.refresh_btn.set_icon_name("view-refresh-symbolic")
      self.back_btn.set_icon_name("go-previous-symbolic")
      self.forward_btn.set_icon_name("go-next-symbolic")

      ##Connect Widgets
      self.search.connect("activate", self.on_search)
      self.action.connect("activate", self.print_something)
      self.back_btn.connect('clicked', self.go_back)
      self.forward_btn.connect('clicked', self.go_forward)
      self.refresh_btn.connect('clicked', self.refresh_page)

      ##Add Button to Header
      self.header.pack_end(self.info_btn)
      self.header.pack_start(self.back_btn)
      self.header.pack_start(self.forward_btn)
      self.header.pack_start(self.refresh_btn)
      self.header.pack_start(self.tab_btn)
      self.header.pack_start(self.search)

      ##Create Web Pages
      self.web_page = WebKit2.WebView()
      self.web_page.load_uri("https://duckduckgo.com")
      self.web_page.connect('notify::estimated-load-progress', self.change_url)
      self.win.set_child(self.web_page)
      self.win.present()

  def run(self):
      self.app.run(None)

  def on_search(self, add):
      add = self.search.get_text()
      if add.startswith("https://") or add.startswith("http://"):
          self.web_page.load_uri(add)
      else:
          add = "https://" + add
          self.web_page.load_uri(add)

  def print_something(self, action, param):
      print("somthing")

  def change_url(self, widget, frame):
      uri = self.web_page.get_uri()
      self.search.set_text(uri)

  def go_back(self, widget):
      self.web_page.go_back()

  def go_forward(self, widget):
      self.web_page.go_forward()

  def refresh_page(self, widget):
      self.web_page.reload()


app = MyApp()
app.run()
