from time import strftime, gmtime
import hmac
import hashlib

class header(object):
    def __new__(self):
        apikey = "c8d704bf-5c4d-465c-8d6c-eea33a3e4127"
        secret = "654b814b-9745-44dd-9b60-994982661168"
        dateNow = strftime('%a, %d %b %Y %H:%M:%S +0000', gmtime())
        hashed = hmac.new(secret, dateNow, hashlib.sha1)
        header = {'x-dnsme-apiKey': apikey, 'x-dnsme-requestDate': dateNow, 'x-dnsme-hmac': hashed.hexdigest()}
        return header