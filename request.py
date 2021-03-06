class request:
    def __init__(self, _str):
        self.headers = _str.split(b"\r\n\r\n")[0].split(b"\r\n")
        headerL = {}
        for header in self.headers:
            if(b": " in header):
                headerL[header.split(b": ")[0]] = header.split(b": ")[1]
            else:
                self.proto = header
        print(headerL)
        self.headers = headerL
        if(len(_str.split(b"\r\n\r\n")) == 2):
            self.body = _str.split(b"\r\n\r\n")[1]
            self.headers[b"Content-Length"] = str(len(self.body)).encode()
        else:
            self.body = None
        self.headers[b"Server"] = b"Why Bro???"

    def compile(self):
        rv = b""
        rv += self.proto + b"\r\n"
        for key in self.headers.keys():
            rv += key
            rv += b": "
            rv += self.headers[key]
            rv += b"\r\n"
        rv += b"\r\n"
        if not self.body is None:
            rv += self.body
        return rv