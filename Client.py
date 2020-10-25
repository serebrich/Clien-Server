import socket
from string import ascii_uppercase
import random

# Func for gen the rand string
def random_string(count_of_letters: int):
    return bytes(
        "".join(random.sample(ascii_uppercase, count_of_letters)), encoding="UTF-8"
    )

# Connect to Server
sock = socket.socket()
sock.connect(("localhost", 8686))

# Main loop - recive the data and send rand string
while True:
    data = sock.recv(1024)
    if data:
        try:
            sock.send(random_string(16))
        except OSError:
            sock.close()