class request:
    def __init__(self, _str):
        self.body = _str.split("\r\n\r\n")[1]
        self.headers = _str.split("\r\n\r\n")[0].split("\r\n")
        headerL = {}
        for header in self.headers:
            if(": " in header):
                headerL[header.split(": ")[0]] = header.split(": ")[1]
                self.headers = headerL
            else:
                self.proto = header
        print(self.proto)
        self.compile()

    def compile(self):
        rv = ""
        rv += self.proto + "\r\n"
        for key in self.headers.keys():
            rv += key
            rv += ": "
            rv += self.headers[key]
            rv += "\r\n"
        rv += "\r\n"
        rv += self.body
        print("\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"")
        print(rv)
        return rv.encode()