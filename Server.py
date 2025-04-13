import random
import socket

PASSWORD = "password123"

class GuessingGameServer:
    def __init__(self, host="0.0.0.0", port=7777):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                conn.sendall("Enter password".encode())
                password = conn.recv(1024).decode().strip()
                if password != PASSWORD:
                    conn.sendall("Wrong password. Connection closing.".encode())
                    continue
                conn.sendall("Password accepted. Start guessing!".encode())

                secret_number = random.randint(1, 100)
                print(f"Generated Number: {secret_number}")
                guesses = 0

                while True:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    try:
                        guess = int(data)
                        guesses += 1
                        if guess < secret_number:
                            response = "Too low!"
                        elif guess > secret_number:
                            response = "Too high!"
                        else:
                            if guesses <= 5:
                                rating = "Excellent"
                            elif guesses <= 20:
                                rating = "Very Good"
                            else:
                                rating = "Good/Fair"
                            response = f"Correct! You win! Guesses: {guesses}. Performance: {rating}"
                            conn.sendall(response.encode())
                            break
                        conn.sendall(response.encode())
                    except ValueError:
                        conn.sendall("Invalid input! Please enter a number.".encode())

    def stop(self):
        self.server_socket.close()

def main():
    server = GuessingGameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.stop()

if __name__ == "__main__":
    main()
