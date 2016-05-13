#!/usr/bin/env python

import argparse
import sys
import string
from time import sleep


LCD_BACKLIGHT = '/sys/devices/system/rn_lcd/rn_lcd0/lcd_backlight'
LCD = ['/sys/devices/system/rn_lcd/rn_lcd0/lcd_line1',
       '/sys/devices/system/rn_lcd/rn_lcd0/lcd_line2']
POWER_LED = '/sys/devices/system/rn_button/rn_button0/led1'
BACKUP_LED = '/sys/devices/system/rn_button/rn_button0/led0'
DISK_LED = ['/sys/devices/system/rn_disk/rn_disk0/disk1',
            '/sys/devices/system/rn_disk/rn_disk0/disk2',
	    '/sys/devices/system/rn_disk/rn_disk0/disk3',
	    '/sys/devices/system/rn_disk/rn_disk0/disk4']


def write_to_file(filename, output):
    with open(filename, 'wb') as file_:
        file_.write(output)

def control(ctrl, off=False):
    """Control a file-based device using 0 or 1 strings.
    """
    output = off and '0' or '1'
    write_to_file(ctrl, output)

def backlight(off=False):
    """Turn backlight on or off. Turns on by default.

    Backlight will automatically turn off after a preset period of time.
    Re-run this function at relevant intervals to keep the backlight on.
    Beware that extended use of this or any LCD may result in burn in.
    """
    control(LCD_BACKLIGHT, off)

def power_led(off=False):
    """Turns the front power LED on or off. Turns on by default.
    """
    control(POWER_LED, off)

def backup_led(off=False):
    """Turns the front backup LED on or off.  Turns on by default.
    """
    control(BACKUP_LED, off)

def disk_led(disk, off=False):
    """Turns a front disk LED on or off.  Turns on by default.

    Arguments/Keywords

    disk
        Disk number of the LED you want to control.  Disk counts start at 1, so
	the argument matches the physical number on your front panel (if an NVX ;).
    off
        Boolean-like value to determine whether to turn this off.  Default: False.
    """
    control(DISK_LED[disk-1], off)
    
def scroll_string(outputs, line_number=1, speed=0.25, max_length=18):
    """Scroll a string on the LCD display.

    Arguments/Keywords

    outputs
       Iterable of strings to output one after another.  The display line will
       clear before each subsequent string.
    line_number
       The LCD line to display on.  Typically either 1 or 2. Default: 1.
    speed
       How fast, in seconds, to scroll each character across.  For the NVX,
       the LCD refresh rate means the default speed is around the most
       readable.  Default: 0.25.
    max_length
       The maximum width, in characters, of the LCD screen.  Default: 18 (NVX).

    """
    for output in outputs:
        i = 0
        while i < len(output):
	    #Keep the backlight on by updating every so often 
	    if i % 5 == 0: backlight()

            line = ('{:<' + str(max_length) + '}').format(output[i:i+max_length])
            write_to_file(LCD[line_number-1], line)
            i = i + 1
            sleep(speed)

    backlight(off=True)


def scroll_string_main():
    parser = argparse.ArgumentParser(description="Download ReadyNAS configuration as backup")
    parser.add_argument('outputs', nargs='*', 
                        help="List of strings to output one after another. The display will clear before each subsequent string.")
    parser.add_argument('--line-number', '-l',
                        help="Line number to output the given message to.",
                        type=int,
                        default=1)
    parser.add_argument('--speed', '-s',
                        help="Speed, in seconds, to scroll each character across the display.",
                        type=int,
                        default=0.25)
    parser.add_argument('--max_length', '-m',
                        help="Maximum width in number of characters of the LCD screen.",
                        type=int,
                        default=18)

    args = parser.parse_args()
    scroll_string(**vars(args))


