from uuid import getnode as getmac
from gpsoauth import perform_master_login, perform_oauth

device_id = _get_android_id()

def get_master_token(username, password):
    res = perform_master_login(username, password, device_id)
    if 'Token' not in res:
        return None
    return res['Token']


def get_access_token(username, master_token):
    res = perform_oauth(
        username, master_token, device_id,
        app='com.google.android.apps.chromecast.app',
        service='oauth2:https://www.google.com/accounts/OAuthLogin',
        client_sig='24bb24c05e47e0aefa68a58a766179d9b613a600'
    )
    if 'Auth' not in res:
        return None
    return res['Auth']

def _get_android_id():
    mac_int = getmac()
    if (mac_int >> 40) % 2:
        raise OSError("a valid MAC could not be determined."
                      " Provide an android_id (and be"
                      " sure to provide the same one on future runs).")

    android_id = _create_mac_string(mac_int)
    android_id = android_id.replace(':', '')
    return android_id


def _create_mac_string(num, splitter=':'):
    mac = hex(num)[2:]
    if mac[-1] == 'L':
        mac = mac[:-1]
    pad = max(12 - len(mac), 0)
    mac = '0' * pad + mac
    mac = splitter.join([mac[x:x + 2] for x in range(0, 12, 2)])
    mac = mac.upper()
    return mac

