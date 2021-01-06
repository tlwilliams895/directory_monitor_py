#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = """T.L. Williams(tlwilliams895) completed assessment with
            Deidre Boddie and Dessance Chandler
            Received help from Marcus Chiriboga, SE Coach"""

import sys
import logging
import signal
import time
import os
import argparse
import errno

exit_flag = True
# This variable will be available for the duration
state = {}

def search_for_magic(filename, start_line, magic_string):
    # Your code here - call from watch_dir
    return


def watch_directory(path, magic_string, extension, interval):
    # Your code here
    # search_4_magic = search_for_magic()
    return


def create_parser():
    parser =  argparse.ArgumentParser()
    parser.add_argument("-i", default = "3", help="polling interval")
    parser.add_argument("magic_str", help="magic text")
    parser.add_argument("ext", help="directory to search") 
    parser.add_argument("-p", "--path", default = ".txt", help="directory to watch")

    return parser


def signal_handler(sig_num, frame):
    # Your code here
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    logger.warn('Signal Received: ' + signal.Signals(sig_num).name)

    return


def main(args):
    # Your code here
    # Hook into these two signals from the OS
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    parser = create_parser()
    if not args:
        parser.print_usage()
        sys.exit(1)
    
    parsed_args = parser.parse_args(args)
    print(parsed_args)

    while not exit_flag:
        try:
            # call my directory watching function
            pass
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        # time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start

    return


if __name__ == '__main__':
    main(sys.argv[1:])
