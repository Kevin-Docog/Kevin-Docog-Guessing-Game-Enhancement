import socket
import time

class BotClient:
    def __init__(self, host="192.168.203.48", port=7777, password="password123"):
        self.host = host
        self.port = port
        self.password = password

    def play(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bot_socket:
            bot_socket.connect((self.host, self.port))
            print(bot_socket.recv(1024).decode())
            bot_socket.sendall(self.password.encode())
            response = bot_socket.recv(1024).decode()
            print(response)
            if "accepted" not in response:
                return

            low = 1
            high = 100
            while low <= high:
                guess = (low + high) // 2
                print(f"Bot guesses: {guess}")
                bot_socket.sendall(str(guess).encode())
                response = bot_socket.recv(1024).decode()
                print(response)
                if "Correct!" in response:
                    break
                elif "Too low" in response:
                    low = guess + 1
                elif "Too high" in response:
                    high = guess - 1
                time.sleep(0.5)

def main():
    bot = BotClient()
    try:
        bot.play()
    except KeyboardInterrupt:
        print("Bot stopped.")

if __name__ == "__main__":
    main()
