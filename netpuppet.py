import asyncio
import socket
import struct
import sys

class Remote:
    def __init__(self, host, port, timeout=10, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)

    def _debug_print(self, data, prefix=""):
        if self.debug:
            print(prefix + repr(data))

    def send(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self._debug_print(data, prefix=">> ")
        self.sock.sendall(data)

    def sendline(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.send(data + b'\n')

    def recv(self, size=1024):
        data = self.sock.recv(size)
        self._debug_print(data, prefix="<< ")
        return data

    def recvuntil(self, delim, drop=False):
        if isinstance(delim, str):
            delim = delim.encode('utf-8')
        data = b""
        while not data.endswith(delim):
            try:
                chunk = self.sock.recv(1)
            except socket.timeout:
                break
            if not chunk:
                break
            data += chunk
        self._debug_print(data, prefix="<< ")
        if drop and data.endswith(delim):
            return data[:-len(delim)]
        return data

    readuntil = recvuntil

    def recvline(self, drop_newline=False):
        return self.recvuntil(b'\n', drop=drop_newline)

    readline = recvline

    def sendafter(self, delim, data):
        self.recvuntil(delim)
        self.send(data)

    def sendlineafter(self, delim, data):
        self.recvuntil(delim)
        self.sendline(data)

    async def interactive(self):
        print("[*] Entering async interactive mode. Press CTRL+C to exit.")
        self.sock.setblocking(False)
        loop = asyncio.get_running_loop()
        try:
            while True:
                sock_task = loop.create_task(loop.sock_recv(self.sock, 4096))
                input_task = loop.run_in_executor(None, sys.stdin.readline)
                done, pending = await asyncio.wait(
                    [sock_task, input_task],
                    return_when=asyncio.FIRST_COMPLETED
                )
                if sock_task in done:
                    data = sock_task.result()
                    if data:
                        sys.stdout.write(data.decode('utf-8', errors='ignore'))
                        sys.stdout.flush()
                    else:
                        print("\n[*] Connection closed by remote host.")
                        for task in pending:
                            task.cancel()
                        break
                    for task in pending:
                        task.cancel()
                elif input_task in done:
                    line = input_task.result()
                    if line:
                        self.send(line)
                    for task in pending:
                        task.cancel()
        except KeyboardInterrupt:
            print("\n[*] Exiting interactive mode.")
        finally:
            self.close()

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

def remote(host, port, timeout=10, debug=False):
    return Remote(host, port, timeout=timeout, debug=debug)

connect = remote

p8  = lambda x, endian="little": struct.pack("<B" if endian == "big" else "<B", x)
p16 = lambda x, endian="little": struct.pack(">H" if endian == "big" else "<H", x)
p32 = lambda x, endian="little": struct.pack(">I" if endian == "big" else "<I", x)
p64 = lambda x, endian="little": struct.pack(">Q" if endian == "big" else "<Q", x)

u8  = lambda x, endian="little": struct.unpack(">B" if endian == "big" else "<B", x)[0]
u16 = lambda x, endian="little": struct.unpack(">H" if endian == "big" else "<H", x)[0]
u32 = lambda x, endian="little": struct.unpack(">I" if endian == "big" else "<I", x)[0]
u64 = lambda x, endian="little": struct.unpack(">Q" if endian == "big" else "<Q", x)[0]
