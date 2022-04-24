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
      self.app.connect('activate', self.new_page)
      GLib.set_application_name(app_title)
      self.count = 0

  def on_activate(self, app):
      self.win = Gtk.ApplicationWindow(application=app)
      self.win.set_default_size(600, 600)

      ##Create Widgets for Header
      self.tab_btn = Gtk.Button(label="Tab")
      self.refresh_btn = Gtk.Button(label="Refresh")
      self.back_btn = Gtk.Button(label="Back")
      self.forward_btn = Gtk.Button(label="Forward")
      self.search = Gtk.SearchEntry()
      self.info_btn = Gtk.MenuButton()
      self.notebook = Gtk.Notebook()

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
      self.tab_btn.connect("clicked", self.new_page)

      ##Add Button to Header
      self.header.pack_end(self.info_btn)
      self.header.pack_start(self.back_btn)
      self.header.pack_start(self.forward_btn)
      self.header.pack_start(self.refresh_btn)
      self.header.pack_start(self.tab_btn)
      self.header.pack_end(self.search)

      self.win.set_child(self.notebook)
      self.win.present()

  def run(self):
      self.app.run(None)

  def on_search(self, add):
      add = self.search.get_text()
      if add.startswith("https://") or add.startswith("http://") or add.startswith("https://www.") or add.startswith("http://www."):
          self.web_page.load_uri(add)
      else:
          if add.endswith(".com") or add.endswith(".in") or add.endswith(".org"):
              add = "https://www." + add
              self.web_page.load_uri(add)
          else:
              if self.word_in(add):
                  add.replace(" ", "+")
                  add = "https://duckduckgo.com/?q="+add+"&t=h_&ia=web"
                  self.web_page.load_uri(add)
              else:
                  add = "https://duckduckgo.com/?q="+add+"&t=h_&ia=web"
                  self.web_page.load_uri(add)

  def word_in(self,s):
      return " " not in s


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

  def new_page(self,button):
      self.web_page = WebKit2.WebView()
      self.web_page.load_uri("https://duckduckgo.com")
      self.web_page.connect('notify::estimated-load-progress', self.change_url)

      self.newpage = Gtk.ScrolledWindow()
      self.newpage.set_child(self.web_page)
      self.box = Gtk.Box()
      self.title = Gtk.Label(label="New Tab")
      self.close_btn = Gtk.Button(label="New Tab")
      self.close_btn.set_icon_name("window-close-symbolic")
      self.close_btn.connect("clicked", self.on_tab_close)
      self.box.append(self.title)
      self.box.append(self.close_btn)
      self.notebook.append_page(self.newpage,self.box)
      self.count += 1

  def on_tab_close(self,button):
      self.notebook.remove_page(self.notebook.get_current_page())
      self.count -= 1

app = MyApp()
app.run()
