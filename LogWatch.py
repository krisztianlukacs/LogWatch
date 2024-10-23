#!/usr/bin/env python3

import time
import json
import sys
import re
import argparse

from rich.console import Console
from rich import * # Python Rich Library pip3 install rich
console = Console()

try:
    from colorama import init, Fore, Style
except ImportError:
    print("The 'colorama' module is required to run the program. Install it with the following command: 'pip install colorama'")
    sys.exit(1)

def load_config(config_file):
    """Loads the JSON configuration file and creates a string-color mapping."""
    with open(config_file, 'r') as f:
        config = json.load(f)
    color_map = {}
    for item in config.get('strings', []):
        text = item['text']
        color = item['color'] #.upper()
        #color_code = getattr(Fore, color, '')
        #if color_code:
            #color_map[text] = color_code
        color_map[text] = color
        #else:
        #    print(f"Warning: Unknown color '{color}' in the configuration file.")
    return color_map

def follow(file):
    """Follows the file and returns new lines."""
    file.seek(0, 2)  # Move to the end of the file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def main():
    parser = argparse.ArgumentParser(description='Log Watcher with color.')
    parser.add_argument('logfile', help='The log file to watch.')
    parser.add_argument('config', help='The JSON configuration file containing strings and colors.')
    parser.add_argument('filter', help='Displays only the rows that contain this string')
    args = parser.parse_args()
    if not args.filter: args.filter = None

    init(autoreset=True)  # Initialize colorama

    color_map = load_config(args.config)

    # Create a regular expression for string matching
    pattern = re.compile('|'.join(re.escape(key) for key in color_map.keys()))

    try:
        with open(args.logfile, 'r') as logfile:
            loglines = follow(logfile)
            for line in loglines:
                line = line.rstrip()

                if args.filter and args.filter not in line:
                    continue

                # Coloring the found strings
                def replacer(match):
                    word = match.group(0)
                    color = color_map.get(word, '')
                #    return f"{color}{word}{Style.RESET_ALL}"
                    return f"[{color}]{word}[/{color}]"
                colored_line = pattern.sub(replacer, line)
                console.print(colored_line)

    except KeyboardInterrupt:
        print("\nThe program stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
    