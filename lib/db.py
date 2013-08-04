# -*- coding: utf-8 -*-
import os

import sqlite3
import cherrypy

class DBPlugin(cherrypy.process.plugins.SimplePlugin):

    first_run = True

    def __init__(self, bus, base_dir):
        cherrypy.process.plugins.SimplePlugin.__init__(self, bus)
        self.base_dir = base_dir

    def start(self):
        self.bus.subscribe('start_thread', self.start_thread)
        self.bus.subscribe('stop_thread', self.stop_thread)

    def stop(self):
        self.bus.unsubscribe('start_thread', self.start_thread)
        self.bus.unsubscribe('stop_thread', self.stop_thread)

    def start_thread(self, index):
        cherrypy.thread_data.sql = sqlite3.connect(os.path.join(self.base_dir,
                                                                'qdb.db'))
        if self.first_run:
            self.first_run = False
            c = cherrypy.thread_data.sql.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS "quotes" ('
                      '"id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                      '"date" INTEGER NOT NULL,'
                      '"quote" TEXT NOT NULL,'
                      '"approved" INTEGER NOT NULL DEFAULT (0),'
                      '"rate" INTEGER DEFAULT (0),'
                      '"voters" TEXT);')
            c.execute('CREATE TABLE IF NOT EXISTS "voters" ('
                      '"vid" INTEGER NOT NULL,'
                      '"ip" INTEGER NOT NULL);')
            c.execute('CREATE TABLE IF NOT EXISTS "admins" ('
                      '"login" TEXT NOT NULL,'
                      '"pass" TEXT NOT NULL);')
            cherrypy.thread_data.sql.commit()
            c.execute('SELECT * FROM admins')
            if c.fetchone() is None:
                import hashlib
                pwd = hashlib.sha256("admin".encode('utf-8')).hexdigest()
                c.execute('INSERT INTO admins VALUES (?,?)', ['admin', pwd])
                cherrypy.thread_data.sql.commit()
            c.close()


    def stop_thread(self, index):
        cherrypy.thread_data.sql.commit()
        cherrypy.thread_data.sql.close()
