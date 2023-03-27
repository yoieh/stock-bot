from avanza import Avanza
import pyotp
import hashlib


def get_avanza_data(username, password, totp_secret):
    totp = pyotp.TOTP(totp_secret, digest=hashlib.sha1)
    avanza = Avanza({
        'username': username,
        'password': password,
        'totpSecret': totp_secret
    })

    overview = avanza.get_overview()
    return overview
