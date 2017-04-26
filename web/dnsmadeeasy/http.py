import httplib2

class http():
    def __init__(self, url, method, data, header):
        http = httplib2.Http()
        response, content = http.request(url, method, body=data, headers=header)

