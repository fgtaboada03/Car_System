from flask import Flask, request, jsonify
import time
import json

with open("config.json") as f:
    config = json.load(f)

PORT = config.get("server_port", 5000)
ALLOWED_DEVICES = config.get("allow_devices", [])
LOG_FILE = config.get("log_file", "music_log.txt")
STATE_TIMEOUT = config.get("state_timeout_seconds", 5)

app = Flask(__name__)

playback_state = {
    "device": None,
    "state": "stopped",
    "track": {},
    "last_update": 0
}

def log_event(data):
    """Append JSON event to log file"""
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

@app.route("/now_playing", methods=["POST"])
def now_playing():
    global playback_state

    data = request.json
    if not data:
        return jsonify({"status": "error", "reason": "no JSON received"}), 400

    device = data.get("device")
    if device not in ALLOWED_DEVICES:
        return jsonify({"status": "error", "reason": "device not allowed"}), 403

    # Update playback state
    playback_state["device"] = device
    playback_state["state"] = data.get("state", "stopped")
    playback_state["track"] = data.get("track", {})
    playback_state["last_update"] = time.time()

    # Log it
    log_event(data)

    # Print for debugging
    track = playback_state["track"]
    print(f"[{time.strftime('%H:%M:%S')}] {device} - {playback_state['state']}: "
          f"{track.get('artist', 'Unknown')} - {track.get('title', 'Unknown')} "
          f"({track.get('elapsed',0)}/{track.get('duration',0)})")

    return jsonify({"status": "ok"})

def check_timeout():
    """Mark playback as stopped if no updates in STATE_TIMEOUT"""
    while True:
        now = time.time()
        if playback_state["state"] != "stopped" and (now - playback_state["last_update"]) > STATE_TIMEOUT:
            playback_state["state"] = "stopped"
            print(f"[{time.strftime('%H:%M:%S')}] Playback stopped (timeout)")
        time.sleep(1)

def main():
    import threading
    # Start timeout checker in background
    t = threading.Thread(target=check_timeout, daemon=True)
    t.start()
    # Run Flask server
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
