# netpuppet
netpuppet is a lightweight Python library for remote interaction over TCP sockets. It provides a simple API for sending and receiving data, handling structured binary data, and interacting with remote services efficiently.

## Features
 ✅ Simple and intuitive API for TCP communication<br/>
 ✅ Support for sending and receiving lines, delimited data, and raw bytes<br/>
 ✅ Easy-to-use packing and unpacking utilities for structured binary data<br/>
 ✅ Debugging mode for monitoring communication<br/>
 ✅ Context manager support (with statement)<br/>
 ✅ Interactive asynchronous mode for manual interaction<br/>

## Installation
No installation is required. Simply download or copy the netpuppet.py file and import it into your project.

## Usage

### Basic Connection
```py
from netpuppet import remote

host = "example.com"
port = 1337

p = remote(host, port, debug=True)
p.sendline("Hello, server!")
response = p.recvline()
print("Received:", response.decode())
p.close()
```

### Using as a Context Manager
```py
from netpuppet import remote

with remote("example.com", 1337) as p:
    p.sendline("Hello!")
    print(p.recvline().decode())
```

### Receiving Data Until a Delimiter
```py
p.recvuntil("Username:")
p.sendline("admin")
p.recvuntil("Password:")
p.sendline("supersecret")
```

### Sending Data After Receiving a Prompt
```py
p.sendlineafter("Username:", "admin")
p.sendlineafter("Password:", "supersecret")
```

### Packing and Unpacking Data
```py
from netpuppet import p32, u32

packed = p32(0xdeadbeef)
unpacked = u32(packed)
print(f"Packed: {packed.hex()} | Unpacked: {hex(unpacked)}")
```

### Interactive Mode
```py
import asyncio

async def interact():
    with remote("example.com", 1337) as p:
        await p.interactive()

asyncio.run(interact())
```

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## Author

Developed by Austin Wile.
