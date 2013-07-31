import requests
import simplejson

__author__ = 'khoatran'


class PushAPIRequester:
    APP_ID = 'xxxxxx'
    APP_MASTER_SECRET = 'xxxxxxxxxxxx'

    API_RICH_PUSH = 'https://go.urbanairship.com/api/airmail/send/'
    API_RICH_PUSH_BROADCAST = 'https://go.urbanairship.com/api/airmail/send/broadcast/'

    def push(self, users, alert, title, message):
        payload = {
            'users': users,
            'push': {
                'android': {
                    'alert': alert
                }
            },
            'title': title,
            'message': message,
            'content-type': 'text/html'
        }

        res = requests.post(self.API_RICH_PUSH,
                            data=simplejson.dumps(payload),
                            headers={'content-type': 'application/json'},
                            auth=(self.APP_ID, self.APP_MASTER_SECRET),)
        return res.status_code == 200

    def broadcast(self, alert, title, message):
        payload = {
            'push': {
                'android': {
                    'alert': alert
                }
            },
            'title': title,
            'message': message,
            'content-type': 'text/html'
        }

        res = requests.post(self.API_RICH_PUSH_BROADCAST,
                            data=simplejson.dumps(payload),
                            headers={'content-type': 'application/json'},
                            auth=(self.APP_ID, self.APP_MASTER_SECRET),)

        return res.status_code == 200
