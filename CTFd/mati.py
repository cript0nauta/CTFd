import os
import json
from flask import (
    Blueprint,
    session,
    redirect,
    request,
    url_for)
from CTFd import utils

mati = Blueprint('mati', __name__)

PASSWORDS_PATH = '/etc/esotheric_credentials.json'
SHARED_MSG = (
    'Could not get credentials for your user. Use '
    'the user "shared" with password "ohT6ohleinaingeeVoo2" '
    'to access to a shared account'
)


@mati.route('/esotheric_credentials')
def esotheric_credentials():
    if not utils.authed():
        return redirect(url_for('auth.login', next=request.path))
    if not os.path.exists(PASSWORDS_PATH):
        return '(NOT CONFIGURED) ' + SHARED_MSG
    with open(PASSWORDS_PATH) as fp:
        passwords = json.load(fp)
    user_id = session['id']
    username = 'team%s' % str(user_id).rjust(3, '0')
    try:
        password = passwords[str(user_id)]
    except KeyError:
        return SHARED_MSG
    return 'Username: "%s"; Password: "%s"' % (username, password)
