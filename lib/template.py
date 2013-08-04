# -*- coding: utf-8 -*-
import os

import cherrypy
from mako.lookup import TemplateLookup


class TemplatePlugin(cherrypy.process.plugins.SimplePlugin):

    def __init__(self, bus, base_dir):
        cherrypy.process.plugins.SimplePlugin.__init__(self, bus)
        self.base_dir = base_dir
        self.tpl_dir = os.path.join(self.base_dir, 'template')
        self.cache_dir = os.path.join(self.base_dir, 'cache')
        self.lookup = None

    def start(self):
        self.lookup = TemplateLookup(directories=self.tpl_dir,
                                     module_directory=self.cache_dir,
                                     input_encoding='utf-8',
                                     output_encoding='utf-8')
        self.bus.subscribe('lookup-template', self.get_template)

    def stop(self):
        self.bus.unsubscribe('lookup-template', self.get_template)
        self.lookup = None

    def get_template(self, name):
        return self.lookup.get_template(name)


class TemplateTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_finalize',
                               self._render,
                               priority=30)

    def _render(self, template=None):
        data = cherrypy.response.body or {}
        template = cherrypy.engine.publish('lookup-template', template).pop()

        if template and isinstance(data, dict):
            cherrypy.response.body = template.render(**data)
