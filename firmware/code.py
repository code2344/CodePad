# note to any reviewers, this is circuitpython code.

import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ----------------------------
# Hardware setup
# ----------------------------
# LEDs
NUM_LEDS = 8
LED_PIN = board.GP2
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.2, auto_write=True)

# Switches
switch_pins = [board.GP11, board.GP10, board.GP9]  # Keys 1,2,3
switches = []
for pin in switch_pins:
    sw = digitalio.DigitalInOut(pin)
    sw.direction = digitalio.Direction.INPUT
    sw.pull = digitalio.Pull.UP
    switches.append(sw)

# Keyboard interface
kbd = Keyboard(usb_hid.devices)

# ----------------------------
# LED State Functions
# ----------------------------
def set_led(led_index, color):
    """Set individual LED color."""
    if 0 <= led_index < NUM_LEDS:
        pixels[led_index] = color

def all_off():
    pixels.fill((0,0,0))

# Example colors (RGB)
COLORS = {
    "saved": (0,255,0),
    "unsaved": (255,0,0),
    "error_save": (255,255,0),
    "git_clean": (0,0,255),
    "git_changes": (128,0,128),
    "git_error": (255,0,0),
    "build_success": (0,255,0),
    "build_error": (255,0,0),
    "build_running": (255,255,0),
    "ai_ready": (0,255,255),
    "debug_active": (255,255,0),
    "server_running": (255,128,0),
    "lint_error": (255,0,0),
    "warning": (255,255,0),
    "custom": (255,0,255)
}

# ----------------------------
# Main loop
# ----------------------------
while True:
    # ----------------------------
    # Read switches
    # ----------------------------
    # Switches are active low
    if not switches[0].value:
        # Key1: Save (Ctrl+S)
        kbd.press(Keycode.CONTROL, Keycode.S)
        time.sleep(0.1)
        kbd.release_all()
        # Example: flash LED1 green
        set_led(0, COLORS["saved"])
        time.sleep(0.1)
        set_led(0, (0,0,0))

    if not switches[1].value:
        # Key2: AI Commit
        # This could later trigger a serial message to your PC script
        # For now, simulate LED flash
        set_led(1, COLORS["git_changes"])
        set_led(3, COLORS["ai_ready"])  # LED4 for AI ready
        time.sleep(0.2)
        set_led(1, (0,0,0))
        set_led(3, (0,0,0))

    if not switches[2].value:
        # Key3: Run/Open
        # This could later trigger a script to detect file type and run appropriate program
        # For now, simulate LED3 (build/run) flash
        set_led(2, COLORS["build_running"])
        time.sleep(0.2)
        set_led(2, COLORS["build_success"])

    # Optional: update LED status dynamically here if connected to PC
    # time.sleep small to debounce buttons
    time.sleep(0.05)