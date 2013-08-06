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
                      ' date DESC')
        elif mode == 'best':
            c.execute('SELECT * FROM quotes WHERE approved=1 ORDER BY'
                      ' rate DESC')
        else:
            return {}

        data = {'quotes': c.fetchall(), 'mode': mode}
        c.close()
        return data

    @cherrypy.expose
    @cherrypy.tools.render(template="submit.mako")
    def submit(self, quote=None):
        data = {}
        if quote is not None:
            c = cherrypy.thread_data.sql.cursor()
            import time
            c.execute('INSERT INTO quotes(date,quote) VALUES(?,?)',
                      [int(time.time()), quote])
            c.close()
            cherrypy.thread_data.sql.commit()
            data.update({'sent': True})
        return data

    @cherrypy.expose
    @cherrypy.tools.render(template="admin.mako")
    @cherrypy.tools.auth()
    def admin(self):
        #raise cherrypy.HTTPRedirect("/login")
        c = cherrypy.thread_data.sql.cursor()
        c.execute('SELECT * FROM quotes WHERE approved=0 ORDER BY date ASC')
        data = {'quotes': c.fetchall()}
        c.close()
        return data

    @cherrypy.expose
    @cherrypy.tools.auth()
    def approve(self, id):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('UPDATE quotes SET approved=1 WHERE id=?', [id])
        cherrypy.thread_data.sql.commit()
        c.close()
        return b'OK'

    @cherrypy.expose
    @cherrypy.tools.auth()
    def delete(self, id):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('DELETE FROM quotes WHERE id=?', [id])
        cherrypy.thread_data.sql.commit()
        c.close()
        return b'OK'

    # MAKE IT SECURE!
    @cherrypy.expose
    def voteup(self, id):
        can = self.__user_cannot_vote(id)
        if can:
            return can

        c = cherrypy.thread_data.sql.cursor()
        c.execute('UPDATE quotes SET rate=rate+1 WHERE id=?', [id])
        cherrypy.thread_data.sql.commit()
        c.close()
        self.__add_user_to_voters(id)
        resp = 'OK - rate: %d' % self.__get_current_rating(id)
        return bytes(resp, 'utf-8')

    @cherrypy.expose
    def votedown(self, id):
        can = self.__user_cannot_vote(id)
        if can:
            return can

        c = cherrypy.thread_data.sql.cursor()
        c.execute('UPDATE quotes SET rate=rate-1 WHERE id=?', [id])
        cherrypy.thread_data.sql.commit()
        c.close()
        self.__add_user_to_voters(id)
        resp = 'OK - rate: %d' % self.__get_current_rating(id)
        return bytes(resp, 'utf-8')

    @cherrypy.expose
    @cherrypy.tools.render(template="login.mako")
    def login(self, username=None, password=None):
        if username is not None:
            import hashlib
            pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
            c = cherrypy.thread_data.sql.cursor()
            c.execute('SELECT * FROM admins WHERE login=? AND pass=?',
                      [username, pwd])
            if c.fetchone() is not None:
                cherrypy.session.regenerate()
                cherrypy.session['qdb_username'] = username
                cherrypy.request.login = username
                raise cherrypy.HTTPRedirect('/admin')
        return {}

    @cherrypy.expose
    @cherrypy.tools.auth()
    def change_pwd(self, pwd=None):
        pass

    def __user_cannot_vote(self, id):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('SELECT * FROM quotes WHERE id=?', id)
        res = c.fetchone()
        if res is None:
            c.close()
            return b"Quote not found"

        ip = cherrypy.request.remote.ip
        c.execute('SELECT * from voters WHERE ip=? AND vid=?', [ip, id])
        res = c.fetchone()
        if res is not None:
            c.close()
            return b"Already voted, sorry."
        c.close()
        return False

    def __add_user_to_voters(self, id):
        c = cherrypy.thread_data.sql.cursor()
        ip = cherrypy.request.remote.ip
        c.execute('INSERT INTO voters(vid,ip) VALUES(?,?)', [id, ip])
        cherrypy.thread_data.sql.commit()
        c.close()

    def __get_current_rating(self, id):
        c = cherrypy.thread_data.sql.cursor()
        c.execute('SELECT rate FROM quotes WHERE id=?', [id])
        return c.fetchone()[0]

