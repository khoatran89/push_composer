import web
import hashlib
import sqlite3
import re

import os
AUTH_DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

__author__ = 'khoatran'
__all__ = ['login', 'logout']

pat_alphanumeric = re.compile('^[\w-]+$')


class login:
    def GET(self):
        web.header('Content-Type', 'text/html')
        return """
        <h1>Marathon Push</h1>
        <form method="POST">
        <p>
            <label>Username</label>
            <input type="text" name="username">
        </p>
        <p>
            <label>Password</label>
            <input type="password" name="password">
        </p>
        <p>
            <input type="submit" value="Login">
        </p>
        </form>
        """

    def POST(self):
        data = web.input()

        authdb = sqlite3.connect(AUTH_DB_PATH)
        pwdhash = hashlib.md5(data.password).hexdigest()
        username = data.username
        if not pat_alphanumeric.match(username):
            return """
            <h1>Marathon Push</h1>
            <p><strong>Invalid username</strong></p>
            <a href="/login">Try again</a>
            """

        validated = authdb.execute('select count(username) from users where username=? and password=?',
                               (username, pwdhash)).fetchone()[0] == 1
        authdb.close()

        if validated:
            web.ctx.session.logged_in = True
            web.ctx.session.username = data.username
            raise web.redirect('/compose')
        else:
            web.header('Content-Type', 'text/html')
            return """<p><strong>Username and password do not match</strong></p>
            <a href="/login">Try again</a>"""


class logout:
    def GET(self):
        web.ctx.session.logged_in = False
        web.ctx.session.username = None
        web.header('Content-Type', 'text/html')
        return """
        Logged out!
        <a href="/login">Login again</a>
        """
