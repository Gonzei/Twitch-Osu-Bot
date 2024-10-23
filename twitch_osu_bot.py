import socket
import re
import threading
import time

# region Twitch and osu! Credentials
# Twitch credentials
twitch_server = 'irc.chat.twitch.tv'
twitch_port = 6667
twitch_nickname = ''  # Twitch bot account username
twitch_token = ''  # OAuth token from Twitch Chat OAuth Generator
twitch_channel = ''  # Your Twitch channel (include the #)

# osu! Bancho IRC credentials
bancho_server = 'irc.ppy.sh'
bancho_port = 6667
bancho_nickname = ''  # Your osu! main account username
bancho_password = ''  # IRC password from osu! account settings

# endregion

# Function to connect to osu! Bancho IRC
def connect_to_bancho():
    try:
        bancho_sock = socket.socket()
        bancho_sock.connect((bancho_server, bancho_port))
        bancho_sock.send(f"PASS {bancho_password}\r\n".encode('utf-8'))
        bancho_sock.send(f"NICK {bancho_nickname}\r\n".encode('utf-8'))
        print("Connected to Bancho IRC.")
        return bancho_sock
    except Exception as e:
        print(f"Error connecting to Bancho IRC: {e}")
        return None

# Function to send a message to osu! Bancho IRC
def send_to_bancho(sock, message):
    try:
        irc_message = f"PRIVMSG {bancho_nickname} :{message}\r\n"  # Send to your osu! username
        sock.send(irc_message.encode('utf-8'))
        print(f"Sent message to osu! Bancho: {message}")
    except Exception as e:
        print(f"Error sending message to Bancho: {e}")

# Function to listen for server PINGs and respond, also sends PING to keep alive
def listen_and_ping_bancho(sock):
    ping_interval = 60  # Ping every 60 seconds to keep the connection alive
    last_ping_time = time.time()

    while True:
        # Respond to server PINGs
        try:
            response = sock.recv(2048).decode('utf-8')
            if response.startswith("PING"):
                sock.send(f"PONG {response.split()[1]}\r\n".encode('utf-8'))
                print(f"Responded to PING: {response}")
        except socket.timeout:
            pass

        # Send PING to the server periodically to keep connection alive
        if time.time() - last_ping_time > ping_interval:
            try:
                sock.send(f"PING :bancho.ppy.sh\r\n".encode('utf-8'))
                print("Sent PING to Bancho to keep connection alive.")
                last_ping_time = time.time()
            except Exception as e:
                print(f"Error sending PING to Bancho: {e}")

# Function to connect to Twitch
def connect_to_twitch():
    twitch_sock = socket.socket()
    twitch_sock.connect((twitch_server, twitch_port))
    twitch_sock.send(f"PASS {twitch_token}\r\n".encode('utf-8'))
    twitch_sock.send(f"NICK {twitch_nickname}\r\n".encode('utf-8'))
    twitch_sock.send(f"JOIN {twitch_channel}\r\n".encode('utf-8'))
    return twitch_sock

# Main function to handle Twitch chat commands and song requests
def handle_twitch_chat(twitch_sock, bancho_sock):
    while True:
        response = twitch_sock.recv(2048).decode('utf-8')

        if response.startswith('PING'):
            twitch_sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        
        if len(response) > 0:
            print(response)  # For debugging purposes
            
            # Detect osu! beatmap URLs
            match = re.search(r"https?://osu.ppy.sh/beatmapsets/\d+", response)
            if match:
                song_url = match.group(0)
                print(f"Detected osu! song request: {song_url}")
                send_to_bancho(bancho_sock, song_url)  # Forward the song request to Bancho IRC

# Main function to start the bot
def main():
    # Connect to Twitch and Bancho IRC
    twitch_sock = connect_to_twitch()
    bancho_sock = connect_to_bancho()

    # Start handling Twitch chat
    threading.Thread(target=handle_twitch_chat, args=(twitch_sock, bancho_sock), daemon=True).start()

    # Listen to Bancho IRC for PINGs and keep sending PING to maintain connection
    listen_and_ping_bancho(bancho_sock)

if __name__ == "__main__":
    main()
