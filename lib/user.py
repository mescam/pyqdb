# -*- coding: utf-8 -*-

import cherrypy

SESSION_KEY = 'qdb_username'
class UserTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_handler',
                               self._check_user,
                               priority=30)

    def _check_user(self):
        username = cherrypy.session.get(SESSION_KEY)
        if username is None:
            raise cherrypy.HTTPRedirect('/login')
        return True

