# !/usr/bin/env python3

"""
Dirwatcher - A long-running program
- argparse
- find the files
- write the logger handler
- exception
- long running program
"""

__author__ = """T.L. Williams(tlwilliams895) completed assessment with
        Deidre Boddie and Dessance Chandler; used Python docs, RealPython
        website, SE workshop/demos, and other resources to complete assessment
        """

import sys
import os
import argparse
import logging
import signal
import time
import datetime


"""
The Formatter for logging is responsible for converting a LogRecord
to (usually) a string which can be interpreted by either a human or
an external system.
"""
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)-8s %(lineno)d",
    datefmt="%A, %B %d, %Y--%I:%M:%S%p",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

exit_flag = False

# This variable will be available for the duration for the files being watched
watched_files = {}


def search_for_magic(filename, start_line, magic_string):
    """
    If the magic string is found in a file, your program should log a message
    indicating which file, and the line number within the file where the magic
    text was found. Once a magic text occurrence has been logged, it should
    not be logged again unless it appears in the file as another subsequent
    line entry later on. Don't worry about reporting multiple occurrences of
    the magic string in a single line.
    """
    # Your code here - call from watch_dir
    # start_line = 0
    # return start_line


def watch_directory(path, magic_string, extension, interval):
    """
    Files in the monitored directory may be added, deleted, or appended at any
    time by other processes. Your program should log a message when new files
    appear or other previously-watched files disappear. Assume that files will
    only be changed by appending to them. That is, anything that has previously
    been written to a file will not change. Only new content will be added to
    the end of the file, so you won't have to continually re-check sections of
    a file that you have already checked.
    """
    # Your code here
    # search_4_magic = search_for_magic()
    return


def create_parser():
    """Create the parser and return the argparse CLI options and parameters"""
    parser = argparse.ArgumentParser(
        prog="DirWatcher",
        description="Program will continually search within all files for modifications in the directory.",
        epilog="Enjoy the DirWatcher program! :-)"
        )

    # Add the arguments for dirwatcher
    parser.add_argument("-i", "--interval", default="1",
                        help="Polling interval")

    parser.add_argument("-m", "--magic_text",
                        help="Magic text to search for")

    parser.add_argument("-e", "--ext", default=".txt",
                        help="Filters type of file extension to search within")

    parser.add_argument("-d", "--dir", default="/",
                        help="Specify the directory to watch")
    return parser


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here
    as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if
    the signal is trapped.

    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global exit_flag

    # log the associated signal name
    logger.warning('Signal Received: ' + signal.Signals(sig_num).name)

    exit_flag = True


def main(args):
    parser = create_parser()

    # Execute the parse_args() method
    args = parser.parse_args(args)

    # if not args:
    #     parser.print_usage()
    #     sys.exit(1)

    """
    After the .parse_args() above is executed a Namespace (simple Class
    object/property) is created by default holding attributes for each
    input args received/returned from the command line.
    """
    # print(parsed_args)

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    # Create start_up banner to display info from program
    # File_Name that is running; Add time_stamp from datetime module
    start_time = datetime.datetime.now()
    # Use () to add data as strings, not a tuple
    start_up = (
        "\n" +
        "*" * 100 +
        f"\n\tRunning {__file__}" +
        f"\n\tStarted on {start_time.isoformat()}\n" +
        "*" * 100
    )

    logger.info(start_up)

    while not exit_flag:
        try:
            # call my directory watching function
            # watch_directory()
            logger.info("Info logger running...")
        except KeyboardInterrupt:
            break
        except Exception as err:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error("Exception Message: ", err)
            pass

            # put a sleep inside my while loop so I don't peg the
            # cpu usage at 100%. EX: time.sleep(polling_interval)
            time.sleep(3)

    # final exit point happens here
    # Log a message that we are shutting down

    # Include the overall uptime since program start
    total_runtime = datetime.datetime.now() - start_time
    shut_down = (
        "\n" +
        "*" * 100 +
        f"\n\tStopped at: {__file__}" +
        f"\n\tTotal Runtime: {total_runtime}\n" +
        "*" * 100
    )
    logger.info(shut_down)


# Import guard clause
if __name__ == '__main__':
    main(sys.argv[1:])
