import web
from web import form
from push_api import PushAPIRequester

__author__ = 'khoatran'

render = web.template.render('templates/')

from auth import logout, login

urls = (
    '/static/.*', 'static',  # this is used for development only
    '/login', login,
    '/logout', logout,
    '/compose', 'compose',
    '/*', 'index',
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'))


def session_hook():
    web.ctx.session = session

app.add_processor(web.loadhook(session_hook))


compose_form = form.Form(
    form.Textbox('users', size=100, description='User IDs', class_='input-block-level'),
    form.Textbox('push_alert', form.notnull, description='Push Alert', size=100,
                 class_='input-block-level'),
    form.Textbox('title', form.notnull, description='Title', size=100, class_='input-block-level'),
    form.Textarea('message', form.notnull, description='Message', rows=5, cols=100,
                  class_='input-block-level'),
    form.Checkbox('broadcast', description='', post='Send broadcast message'),
    form.Button('Send', class_='btn btn-primary'),
)


# view decorator
def login_required(view):
    def require_login(*args, **kwargs):
        if web.ctx.session.get('logged_in', False):
            return view(*args, **kwargs)
        else:
            raise web.redirect('/login')
    return require_login


class index:
    def GET(self):
        raise web.redirect('/compose')


class compose:
    @login_required
    def GET(self):
        form = compose_form()
        return render.compose(form)

    @login_required
    def POST(self):
        form = compose_form()
        if not form.validates():
            return render.compose(form)
        else:
            users = form.d.users.split(',')
            push_alert = form.d.push_alert
            title = form.d.title
            message = form.d.message
            broadcast = web.input().has_key('broadcast')

            requester = PushAPIRequester()
            if broadcast:
                success = requester.broadcast(push_alert, title, message)
            else:
                success = requester.push(users, push_alert, title, message)

            if success:
                return 'message sent'
            else:
                return 'failed'


class static:
    def GET(self):
        raise web.seeother('static/' + web.ctx.path)


application = app.wsgifunc()

if __name__ == '__main__':
    app.run()
