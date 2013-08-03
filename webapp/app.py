#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy

class Quote(object):

    def __init__(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.render(template="index.mako")
    def index(self):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('SELECT approved, COUNT(*) FROM quotes GROUP BY approved;')
        data = {'approved%d'%(x[0]): x[1] for x in c.fetchall()}
        if 'approved1' not in data:
            data.update({'approved1': 0})
        if 'approved0' not in data:
            data.update({'approved0': 0})
        c.close()
        return data

    @cherrypy.expose
    @cherrypy.tools.render(template="list.mako")
    def list(self, mode='new', page=1):
        lbound = (page-1)*10
        c = cherrypy.thread_data.sql.cursor()
        if mode == 'new':
            c.execute('SELECT * FROM quotes WHERE approved=1 ORDER BY'
                      ' date DESC LIMIT ?,?', [lbound, lbound + 10])
        elif mode == 'best':
            return {}  # to implement
        else:
            return {}

        data = {'quotes': c.fetchall()}
        c.close()
        return data

    @cherrypy.expose
    @cherrypy.tools.render(template="submit.mako")
    def submit(self, sent=False):
        data = {}
        if sent:
            # do something
            data.update({'sent': True})
        return data

    # MAKE IT SECURE!
    @cherrypy.expose
    def voteup(self, id):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('UPDATE quotes SET rate=rate+1 WHERE id=?', id)
        cherrypy.thread_data.sql.commit()
        c.close()

    @cherrypy.expose
    def votedown(self, id):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('UPDATE quotes SET rate=rate-1 WHERE id=?', id)
        cherrypy.thread_data.sql.commit()
        c.close()

