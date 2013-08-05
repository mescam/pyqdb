#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path
import sys
import argparse

import cherrypy


class Application(object):

    def __init__(self, args):
        self.args = args
        # some directories
        self.base_dir = os.path.normpath(os.path.abspath('.'))
        self.conf_path = os.path.join(self.base_dir, "conf")

        # place for logs and cache
        log_dir = os.path.join(self.base_dir, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        cache_dir = os.path.join(self.base_dir, "logs")
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        sys.path.insert(0, self.base_dir)

        from lib.template import TemplatePlugin, TemplateTool
        cherrypy.tools.render = TemplateTool()
        cherrypy.engine.mako = TemplatePlugin(cherrypy.engine, self.base_dir)
        cherrypy.engine.mako.subscribe()

        from lib.user import UserTool
        cherrypy.tools.auth = UserTool()

        from lib.db import DBPlugin
        cherrypy.engine.db = DBPlugin(cherrypy.engine, self.base_dir)
        cherrypy.engine.db.subscribe()

        #cherrypy.tools.proxy(base=None,
        #                     local='X-Forwarded-Host',
        #                     remote='X-Forwarded-For',
        #                     scheme='X-Forwarded-Proto')
        #cherrypy.tools.proxy.subscribe()

        from webapp.app import Quote
        webapp = Quote()
        self.app = cherrypy.tree.mount(webapp, '/',
                                       os.path.join(self.conf_path, "app.cfg"))

    def run(self):
        cherrypy.config.update(os.path.join(self.conf_path, "http.cfg"))
        if hasattr(cherrypy.engine, "signal_handler"):
            cherrypy.engine.signal_handler.subscribe()
        if hasattr(cherrypy.engine, "console_control_handler"):
            cherrypy.engine.console_control_handler.subscribe()
        cherrypy.engine.start()
        cherrypy.engine.block()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple quotes database app')
    parser.add_argument('-d', action='store_true', default=False,
                        help='run in background (not implemented)')
    parser.add_argument('-p', '--pidfile', action='store', default=False,
                        help='save PID in pidfile')
    Application(parser.parse_args()).run()



