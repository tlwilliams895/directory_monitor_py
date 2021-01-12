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
        Received assistance from Kano Marvel and JT Maupin
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
# Create root logger for program
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)-8s %(lineno)d",
    datefmt="%A, %B %d, %Y--%I:%M:%S%p",
    level=logging.DEBUG
)

# Create module level logger object to send output from logging messages
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Toggle control for infinite while loop
exit_flag = False
# This variable will be available for the duration for the files being watched
watched_files = {}
# Store location/positon of magic text in dictionary variable
# locate_magic_text = {}


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
    # global locate_magic_text


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
    global watched_files
    # global locate_magic_text
    directory = os.path.isdir(path)
    list_dir = os.listdir(path)

    if not directory:
        logger.info(f"Directory Not Found: {path}")
    else:
        # check for correct extension
        files = [file for file in list_dir if file.endswith(extension)]

        # Checks for new files with extension in the dictionary
        for file in files:
            if file not in watched_files:
                watched_files[file] = 0
                logger.info(f"New File: {file} was Found")
            # Use os.path.join() to create a path to direct the file
            new_file = os.path.join(path, file)

            with open(new_file) as f:
                # Accurate line count for tracking
                lines_counted = watched_files[file]
                # Create a counter variable initialized at 0
                line_count = watched_files[file]
                # Retrieve list of all of the lines
                lines = f.readlines()
                # Use for loop to return the line number and text
                for index, line in enumerate(lines[line_count:]):
                    line_count += 1
                    if magic_string in line:
                        ending_line = index + lines_counted + 1
                        logger.info(
                            f"Magic_Text: {magic_string}; Found in file: {file}; Line #{ending_line}"
                            )
                # Use dictionary variable to output the number of files
                watched_files[file] = line_count

        # Deletes file from directory
        del_files = []
        for file in watched_files:
            if file not in files:
                del_files.append(file)
                logger.info(f"File Deleted: {file}")
        for file in del_files:
            del watched_files[file]


def create_parser():
    """
    Create the parser and return the argparse CLI options and parameters
    The ArgumentParser() object will hold all the information necessary to
    parse the command line into Python data types.
    """
    parser = argparse.ArgumentParser(
        prog="DirWatcher",
        description="Program will continually search within all files for modifications in the directory.",
        epilog="Enjoy the DirWatcher program! :-)"
    )

    # Add the arguments for dirwatcher
    parser.add_argument("path", default=".",
                        help="Specify the directory to watch",
                        nargs="?")
    parser.add_argument("magic", default="flow",
                        help="Magic text to search for",
                        nargs="?")

    parser.add_argument("-i", "--interval", default="1",
                        type=int, help="Polling interval")

    parser.add_argument("-e", "--extension", default=".txt",
                        help="Filters type of file extension to search within")

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

    The purpose of the signal_handler() in this Python program is to allow
    the program to control and intercept the signals by listening for the signal
    - To obtain the PID use: ps aux | grep dirwatcher.py
    - To terminate/interupt the program use: kill -SIGTERM or -SIGINT <PID>
    - To obtain any suspended processes use: jobs
    - To continue any suspended process use (% and jobs id [1]): %1
    """
    # Toggle control for infinite while loop global variable
    global exit_flag

    # log the associated signal name
    logger.warning('Signal Received: ' + signal.Signals(sig_num).name)

    exit_flag = True


def main(args):
    # Parse command-line arguments to be used
    parser = create_parser()
    # Execute the parse_args() method
    args = parser.parse_args(args)

    """
    After the .parse_args() above is executed a Namespace (simple Class
    object/property) is created by default holding attributes for each
    input args received/returned from the command line.
    """

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
            # call my directory watching function and parameters
            watch_directory(
                args.path,
                args.magic,
                args.extension,
                args.interval
            )
            # logger.info("Info logger running in try/except")
        except KeyboardInterrupt:
            break
        except FileNotFoundError:
            logger.error("File Not Found")
        except RuntimeError as err:
            logger.error("Received and Logged Runtime Error: ", err)
        except Exception as err:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error("Exception Message: ", err)

            # put a sleep inside my while loop so I don't peg the
            # cpu usage at 100%. EX: time.sleep(polling_interval)
            time.sleep(args.interval)

    # final exit point happens here
    # Log a message that we are shutting down

    # Final exit point happens here
    # Include the overall uptime since program start
    total_runtime = datetime.datetime.now() - start_time
    shut_down = (
        "\n" +
        "*" * 100 +
        f"\n\tStopped at: {__file__}" +
        f"\n\tTotal Runtime: {total_runtime}\n" +
        "*" * 100
    )
    # Log a message that we are shutting down
    logger.info(shut_down)


# Import guard clause
if __name__ == '__main__':
    main(sys.argv[1:])
