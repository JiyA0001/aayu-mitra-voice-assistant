

# 🛠️ Service Management Cheat Sheet  
**Service Name:** `aayu-mitra.service`

This guide explains how to control your voice assistant on the Raspberry Pi and how the service was set up for autostart.

---

## 0. ⚙️ How Autostart Was Set Up (One Time Setup)

The assistant runs automatically on boot using two things:

1. A `start.sh` script that activates the virtual environment and runs Python
2. A systemd service file that tells Linux to run `start.sh` at startup

### A. `start.sh` Script

Location example:

```

/home/pi/aayu-mitra-voice-assistant/start.sh

```

Typical contents:
```bash
#!/usr/bin/env bash

set -euo pipefail

  

# Define project root

PROJECT_DIR="/home/pi/aayu-mitra-voice-assistant"

LOG_FILE="$PROJECT_DIR/start.log"

  

# Log everything to start.log

exec >> "$LOG_FILE" 2>&1

  

echo "===== start.sh $(date) ====="

echo "User: $(whoami)"

echo "Directory: $PROJECT_DIR"

  

# Navigate to project directory

cd "$PROJECT_DIR" || { echo "Failed to cd to $PROJECT_DIR"; exit 1; }

  

# Load environment variables

if [ -f .env ]; then

echo "Loading .env..."

set -o allexport

grep -v '^#' .env | grep -v '^\s*$' | source /dev/stdin

set +o allexport

echo ".env loaded"

else

echo "WARNING: .env not found"

fi

  

# Activate virtual environment

# Prioritize .venv as confirmed by user

if [ -d ".venv" ]; then

echo "Activating .venv..."

source .venv/bin/activate

elif [ -d "venv" ]; then

echo "Activating venv..."

source venv/bin/activate

else

echo "ERROR: Virtual environment not found (looked for '.venv' and 'venv')"

exit 1

fi

  

# Wait for WiFi (Network)

echo "Waiting for internet connection..."

for i in {1..30}; do

if ping -c1 -W1 8.8.8.8 >/dev/null 2>&1; then

echo "Internet connected"

break

fi

echo "Waiting for internet... retry $i/30"

sleep 2

done

  

# Wait for Microphone

echo "Waiting for microphone..."

for i in {1..30}; do

if command -v arecord >/dev/null && arecord -l | grep -q "card"; then

echo "Microphone detected"

break

fi

echo "Waiting for microphone... retry $i/30"

sleep 2

done

  

# Wait for Speaker

echo "Waiting for speaker..."

for i in {1..30}; do

if command -v aplay >/dev/null && aplay -l | grep -q "card"; then

echo "Speaker detected"

break

fi

echo "Waiting for speaker... retry $i/30"

sleep 2

done

  

# Start the application

echo "Starting main_voice_loop.py..."

exec python3 main_voice_loop.py
```

Important points:

-   Activates the Python virtual environment
    
-   Runs the main Python file
    
-   Redirects logs to `start.log`
    

Make sure it is executable:

```bash
chmod +x start.sh

```

----------

### B. systemd Service File

Location:

```
/etc/systemd/system/aayu-mitra.service

```

Example service file:

```ini
[Unit]
Description=Aayu Mitra Voice Assistant
# "sound.target" only loads drivers, not the audio server (PipeWire/Pulse). 
# We rely on the environment variables below to find the server.
After=network-online.target sound.target
Wants=network-online.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/aayu-mitra-voice-assistant

# --- CRITICAL AUDIO FIXES ---
# 1. Point to the user's runtime directory (where the audio socket lives)
Environment="XDG_RUNTIME_DIR=/run/user/1000"

# 2. Force Pygame/SDL to use the PulseAudio (PipeWire) backend
Environment="SDL_AUDIODRIVER=pulseaudio"

# 3. Prevent Pygame from trying to open a video window (helps in headless mode)
Environment="SDL_VIDEODRIVER=dummy"
# -----------------------------

ExecStart=/bin/bash /home/pi/aayu-mitra-voice-assistant/start.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

After creating or editing this file, always run:

```bash
sudo systemctl daemon-reload

```

Enable autostart:

```bash
sudo systemctl enable aayu-mitra.service

```

----------

## 1. 🔄 Applying Code Changes (Python)

If you modify `main_voice_loop.py`, `config.py`, or any file inside `features/`:

1.  Save your changes.
    
2.  Restart the service to load the new code:
    
    ```bash
    sudo systemctl restart aayu-mitra.service
    
    ```
    
3.  Immediately check the logs:
    
    ```bash
    sudo journalctl -u aayu-mitra.service -f
    
    ```
    

**What to expect**

-   **Success:**  
    `🎙️ Starting Elderly Voice Assistant`
    
-   **Failure:**  
    Python errors like `IndentationError` or `ImportError`
    

----------

## 2. ⚡ Basic Controls (Current Session)

Use these commands without rebooting.

Action

Command

Description

Check Status

`sudo systemctl status aayu-mitra.service`

Shows running, failed, or stopped

Start

`sudo systemctl start aayu-mitra.service`

Starts immediately

Stop

`sudo systemctl stop aayu-mitra.service`

Stops the assistant

Restart

`sudo systemctl restart aayu-mitra.service`

Reloads code and restarts

----------

## 3. 🚀 Autostart Controls (Boot Behavior)

Control whether the assistant starts on boot.

Action

Command

Description

Enable Autostart

`sudo systemctl enable aayu-mitra.service`

Starts automatically on reboot

Disable Autostart

`sudo systemctl disable aayu-mitra.service`

Will not start on reboot

----------

## 4. ⚙️ Applying System Configuration Changes

If you edit:

```
/etc/systemd/system/aayu-mitra.service

```

Run:

```bash
sudo systemctl daemon-reload
sudo systemctl restart aayu-mitra.service

```

----------

## 5. 🔍 Viewing Logs (Debugging)

### Option A: Live System Logs

Best for startup issues.

```bash
sudo journalctl -u aayu-mitra.service -f

```

Press `Ctrl + C` to exit.

### Option B: Project Log File

Written by `start.sh`.

```bash
tail -f /home/pi/aayu-mitra-voice-assistant/start.log

```

----------

## 6. 🚨 Emergency Force Stop

If the assistant is stuck:

```bash
sudo systemctl kill -s SIGKILL aayu-mitra.service
sudo systemctl stop aayu-mitra.service

```

