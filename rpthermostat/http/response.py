from http.utils import Codes

class Response:
    def __init__(self, version: Version, code: int, headers: dict[str, str], body: str | Callable):
        self.version = version
        self.code = code
        self.headers = headers
        self.body = body
        
    def __repr__(self) -> str:
        r = f"Response <HTTP/{self.version.major}.{self.version.minor} {self.code}>"
        
        for header, value in self.headers.items():
            r += f"\n{header}: {value}"
            
        return r + ("(...)" if callable(self.body) else self.body) + "\n"
        
    def send(self, s: socket.socket) -> None:
        """/!\\ Assuming Transfer-Encoding: chunked"""
        resp = f"HTTP/{self.version.major}.{self.version.minor} {self.code} {Codes[self.code]}\r\n"
        
        for header, value in self.headers.items():
            resp += f"{header}: {value}\r\n"
            
        resp += "\r\n"
            
        s.send(resp.encode())

        if callable(self.body):
            file = self.body()
            
            chunk, file = file[:1024], file[1024:]
            while chunk:
                chunk = chunk.encode()
                # Send the size of the chunk in hexadecimal, followed by the chunk itself
                s.send(f"{len(chunk):X}\r\n".encode() + chunk + b"\r\n")
                    
                chunk, file = file[:1024], file[1024:]
        
            s.send(b"0\r\n\r\n")  # Send the zero-length chunk to indicate end
        
        elif len(self.body):
            with open(self.body, "rb") as file:
                chunk = file.read(1024)
                while chunk:
                    # Send the size of the chunk in hexadecimal, followed by the chunk itself                   
                    s.send(f"{len(chunk):X}\r\n".encode() + chunk + b"\r\n")
                    
                    chunk = file.read(1024)
        
            s.send(b"0\r\n\r\n")  # Send the zero-length chunk to indicate end