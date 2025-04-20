# Twitch osu! Bot

This guide will walk you through how to set up the **Twitch osu! Bot**, which lets you detect osu! beatmap requests in Twitch chat and send them to osu! via Bancho IRC. Even if you've never coded before, don't worry! This guide covers everything from downloading the necessary tools to running the bot. Let's get started!

---

## What You Need:

### 1. **Python**

Python is the programming language the bot is written in. You’ll need to install it on your computer.

- **Download Python**:Go to the official Python website - https://www.python.org/downloads/
  Click the big yellow button that says "Download Python." It will download an installer for your computer.
- **Install Python**:
  After the installer downloads, open it. Make sure to **check the box** that says **"Add Python to PATH"** before clicking "Install Now."

---

### 2. **An IDE (Code Editor)**

An IDE (Integrated Development Environment) is a program that lets you write and run code. We recommend using **Visual Studio Code** (VSCode) because it’s beginner-friendly.

- **Download Visual Studio Code (VSCode)**:Go to the official VSCode website - https://code.visualstudio.com/Download
  Choose your operating system (Windows, macOS, or Linux) and download it.
- **Install VSCode**:
  After downloading, open the installer and follow the instructions to install VSCode on your computer.

---

### 3. **Twitch and osu! Accounts**

You’ll need accounts for both Twitch and osu! to run the bot.

- **Twitch Account**:Go to [Twitch](https://www.twitch.tv/) and create an account if you don’t have one.
- **osu! Account**:
  Go to [osu!](https://osu.ppy.sh/home) and create an account if you don’t have one.

---

### 4. **Twitch OAuth Token**

The bot needs permission to interact with your Twitch chat. For that, we need an OAuth token.

- **Generate a Twitch OAuth Token**:
  1. Go to https://twitchtokengenerator.com/
  2. Click "Connect with Twitch" and log into your Twitch account.
  3. After logging in, it will give you an access token. Copy this token.

---

### 5. **osu! IRC (Bancho) Password**

osu! has an IRC (Internet Relay Chat) server called Bancho. You’ll need a password for the bot to connect.

- **Get Your osu! IRC Password**:
  1. Go to your osu! profile
  2. Scroll down until you find **"IRC Authentication"**.
  3. Copy your **Bancho IRC password**.

---


### 6. **osu! API Credentials**

- **Get Your osu! API Credentials**:

  1. Go to your osu! profile
  2. Scroll down to **"OAuth Applications"** → click  **New OAuth Application**

  * **Name:** Anything (e.g. “Twitch Bot”)
  * **Redirect URI:** Put `http://localhost`

  3. Copy your Client ID and Client Secret.

---

## Setting Up the Bot:

### 1. **Download the Bot Code**

- **Download the Code**:
  Download the bot’s code from this repository or the ZIP file that contains the `twitch_osu_bot.py` file.

### 2. **Open the Code in VSCode**

- **Open VSCode**:Once you have VSCode installed, open it.
- **Open the Bot Code**:
  In VSCode, click on **File** > **Open Folder**. Choose the folder where the `twitch_osu_bot.py` file is located.

---

### 3. **Install Python Libraries**

Python libraries are packages of code that the bot needs to run.

- **Install Required Libraries**:
  1. In VSCode, open the terminal by clicking **View** > **Terminal**.
  2. In the terminal, type this command and press **Enter**:
     ```
     pip install ossapi requests socket re
     ```

---

### 4. **Set Up the Bot Code**

Now we need to add your Twitch and osu! information to the bot code.

- **Open the Bot Code**:In VSCode, open the `twitch_osu_bot.py` file.
- **Edit Your Information**:

  1. **Twitch Username**:Find the line that says `twitch_nickname = ''` and replace it with your Twitch bot’s username (inside the quotes). You may also use your own username to avoid creating a new account.

     Example:

     ```python
     twitch_nickname = 'gonzeiBot'
     ```
  2. **Twitch OAuth Token**:Find the line that says `twitch_token = ''` and paste the OAuth token you copied earlier (inside the quotes).

     Example:

     ```python
     twitch_token = 'oauth:your_token_here'
     ```
  3. **Twitch Channel**:Find the line that says `twitch_channel = ''` and enter your Twitch channel (inside the quotes). Be sure to include the `#` symbol.

     Example:

     ```python
     twitch_channel = '#your_twitch_channel'
     ```
  4. **osu! Username**:Find the line that says `bancho_nickname = ''` and replace it with your osu! username (inside the quotes).

     Example:

     ```python
     bancho_nickname = 'your_osu_username'
     ```
  5. **osu! IRC Password**:
     Find the line that says `bancho_password = ''` and paste your osu! Bancho IRC password (inside the quotes).

     Example:

     ```python
     bancho_password = 'your_osu_irc_password'
     ```

---

### 5. **Run the Bot**

Now you’re ready to run the bot!

- **Run the Bot**:
  1. In VSCode, open the terminal by clicking **View** > **Terminal**.
  2. In the terminal, type this command and press **Enter**:
     ```
     python twitch_osu_bot.py
     ```

If everything is set up correctly, the bot will connect to both Twitch chat and osu! Bancho IRC. The bot will detect any osu! beatmap URLs shared in Twitch chat and send them to osu! Bancho IRC automatically.

---

Troubleshooting:

- **If you see an error message**:Double-check that you correctly entered your Twitch and osu! information in the bot code.
- **If the bot isn’t responding**:
  Ensure that your Twitch bot account has moderator privileges in your Twitch channel.
