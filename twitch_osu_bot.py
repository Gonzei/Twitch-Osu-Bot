import socket
import re
import threading
import time
import requests

# region Twitch and osu! Credentials
# Twitch credentials
twitch_server = 'irc.chat.twitch.tv'
twitch_port = 6667
twitch_nickname = ''  # Twitch bot account username
twitch_token = 'oauth:'  # OAuth token from Twitch Chat OAuth Generator (make sure to do "oauth:...")
twitch_channel = ''  # Your Twitch channel (include the #)

# osu! Bancho IRC credentials
bancho_server = 'irc.ppy.sh'
bancho_port = 6667
bancho_nickname = ''  # Your osu! main account username
bancho_password = ''  # IRC password from osu! account settings

osu_client_id = ''
osu_client_secret = ''
osu_username = ''  # Exact osu! username, case-sensitive

# Discord Invite Link 
discord_link = ""

# endregion

def get_now_playing_from_api():
    try:
        # Step 1: Authenticate
        auth_response = requests.post("https://osu.ppy.sh/oauth/token", json={
            "client_id": osu_client_id,
            "client_secret": osu_client_secret,
            "grant_type": "client_credentials",
            "scope": "public"
        })
        access_token = auth_response.json()["access_token"]

        # Step 2: Get user ID
        user_response = requests.get(
            f"https://osu.ppy.sh/api/v2/users/{osu_username}/osu",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_id = user_response.json()["id"]

        # Step 3: Get recent score
        recent_response = requests.get(
            f"https://osu.ppy.sh/api/v2/users/{user_id}/scores/recent?limit=1",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        scores = recent_response.json()

        if not scores:
            return "🛑 No recent plays found (or the map wasn't finished)."

        score = scores[0]
        beatmap = score.get("beatmap")
        beatmapset_id = beatmap.get("beatmapset_id") if beatmap else None

        if not beatmapset_id:
            return "❌ Could not find beatmapset ID."

        # Step 4: Grab page HTML and parse title manually
        url = f"https://osu.ppy.sh/beatmapsets/{beatmapset_id}"
        page = requests.get(url).text

        # Extract content from <title> tag
        start = page.find("<title>")
        end = page.find("</title>")
        if start == -1 or end == -1:
            return f"🎶 osu! map: {url}"

        raw_title = page[start + 7:end].strip()
        clean_title = raw_title.replace(" · Beatmap info | osu!", "").strip()

        return f"🎶 {clean_title} → {url}"

    except Exception as e:
        return f"❌ Error getting now playing: {str(e)}"

# Bancho IRC connection
def connect_to_bancho():
    try:
        bancho_sock = socket.socket()
        bancho_sock.connect((bancho_server, bancho_port))
        bancho_sock.send(f"PASS {bancho_password}\r\n".encode('utf-8'))
        bancho_sock.send(f"NICK {bancho_nickname}\r\n".encode('utf-8'))
        print("✅ Connected to Bancho IRC.")
        return bancho_sock
    except Exception as e:
        print(f"❌ Error connecting to Bancho IRC: {e}")
        return None

# Send song to Bancho
def send_to_bancho(sock, message):
    try:
        irc_message = f"PRIVMSG {bancho_nickname} :{message}\r\n"
        sock.send(irc_message.encode('utf-8'))
        print(f"➡️ Sent to Bancho: {message}")
    except Exception as e:
        print(f"❌ Error sending message to Bancho: {e}")

# Keep Bancho alive
def listen_and_ping_bancho(sock):
    ping_interval = 60
    last_ping_time = time.time()

    while True:
        try:
            response = sock.recv(2048).decode('utf-8')
            if response.startswith("PING"):
                sock.send(f"PONG {response.split()[1]}\r\n".encode('utf-8'))
                print(f"🔁 Responded to PING: {response}")
        except socket.timeout:
            pass

        if time.time() - last_ping_time > ping_interval:
            try:
                sock.send(f"PING :bancho.ppy.sh\r\n".encode('utf-8'))
                print("📡 Sent PING to Bancho.")
                last_ping_time = time.time()
            except Exception as e:
                print(f"❌ Error pinging Bancho: {e}")

# Twitch connection
def connect_to_twitch():
    twitch_sock = socket.socket()
    twitch_sock.connect((twitch_server, twitch_port))
    twitch_sock.send(f"PASS {twitch_token}\r\n".encode('utf-8'))
    twitch_sock.send(f"NICK {twitch_nickname}\r\n".encode('utf-8'))
    twitch_sock.send(f"JOIN {twitch_channel}\r\n".encode('utf-8'))
    return twitch_sock

# Twitch command handler
def handle_twitch_chat(twitch_sock, bancho_sock):
    while True:
        response = twitch_sock.recv(2048).decode('utf-8')

        if response.startswith('PING'):
            twitch_sock.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))

        if len(response) > 0:
            print(response)

            # Detect beatmap request links
            match = re.search(r"https?://osu.ppy.sh/beatmapsets/\d+", response)
            if match:
                song_url = match.group(0)
                print(f"🎵 Detected song request: {song_url}")
                send_to_bancho(bancho_sock, song_url)

            # Handle !np command
            if "!np" in response.lower():
                now_playing = get_now_playing_from_api()
                twitch_sock.send(f"PRIVMSG {twitch_channel} :{now_playing}\r\n".encode('utf-8'))

            # Handle !discord command
            if "!discord" in response.lower():
                twitch_sock.send(f"PRIVMSG {twitch_channel} :Join our Discord! → {discord_link}\r\n".encode('utf-8'))

# Start bot
def main():
    twitch_sock = connect_to_twitch()
    bancho_sock = connect_to_bancho()
    threading.Thread(target=handle_twitch_chat, args=(twitch_sock, bancho_sock), daemon=True).start()
    listen_and_ping_bancho(bancho_sock)

if __name__ == "__main__":
    main()