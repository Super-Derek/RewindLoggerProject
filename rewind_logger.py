# rewind_logger.py
import time
import threading
from inputs import get_gamepad

# Constants
L_BUTTON_CODE = "BTN_TL"  # This is usually the L button on gamepads
LOG_FILENAME = "rewind_log.txt"

# Variables
rewind_active = False
rewind_events = []
start_time = time.time()

def format_time(seconds):
    # Convert seconds to HH:MM:SS.MS
    ms = int((seconds % 1) * 1000)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"

def log_rewind(event_type, timestamp):
    with open(LOG_FILENAME, "a") as f:
        f.write(f"{event_type} at {format_time(timestamp)}\n")

def listen_for_controller():
    global rewind_active
    while True:
        events = get_gamepad()
        for event in events:
            if event.code == L_BUTTON_CODE:
                now = time.time() - start_time
                if event.state == 1 and not rewind_active:
                    rewind_active = True
                    print(f"Rewind START at {format_time(now)}")
                    log_rewind("START", now)
                elif event.state == 0 and rewind_active:
                    rewind_active = False
                    print(f"Rewind END at {format_time(now)}")
                    log_rewind("END", now)

def main():
    print("Starting Rewind Logger...")
    print("Get ready to start recording...")

    # 5-second countdown
    for i in range(5, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)

    print("Recording and logging STARTED! Begin gameplay now.")
    listen_for_controller()


if __name__ == "__main__":
    main()
