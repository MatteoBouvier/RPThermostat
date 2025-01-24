from http.utils import validate, get_version, Methods, Headers

class Request:
    def __init__(self, method: str, path: str, version: Version, headers: dict[str, str]):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        
    def __repr__(self) -> str:
        r = f"Request <{self.method} {self.path} HTTP/{self.version.major}.{self.version.minor}>"
        
        for header, value in self.headers.items():
            r += f"\n{header}: {value}"
            
        return r + "\n"
        
    @staticmethod
    def from_raw(text: str) -> Request:
        h, *headers = text.split("\n")
        method, path, version = h.split(" ")
        
        parsed_headers = {}
        for line in headers:
            line = line.strip()
            if line:
                name, value = line.split(": ")
                parsed_headers[validate(name, Headers)] = value
        
        return Request(validate(method, Methods), path, get_version(version), parsed_headers)
    
    @staticmethod
    def get(s: socket.socket) -> Request | None:
        data = s.recv(1024).decode("utf-8")
        if not data:
            return None
        
        return Request.from_raw(data)