import requests
import simplejson

__author__ = 'khoatran'


class PushAPIRequester:
    # REMOVE TO HIDE THESE INFORMATION BEFORE PUSHING CODE
    APP_ID = 'fwL2yQz9Rm2uA-Fzr2cLQg'
    APP_MASTER_SECRET = 'K92ivWQqQxmskNGsrYw-gA'

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

        print res.status_code
        print res.text

        return res.status_code == 200
