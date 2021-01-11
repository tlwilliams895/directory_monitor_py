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
# Create root logger for program
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)-8s %(lineno)d",
    datefmt="%A, %B %d, %Y--%I:%M:%S%p %Z",
    level=logging.DEBUG
)

# Create module level logger object to send output from logging messages
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Toggle control for infinite while loop
exit_flag = False
# This variable will be available for the duration for the files being watched
watching_files = {}


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
    # Create search_4_magic = search_for_magic()
    dir_files = os.path.listdir(path)

    # Files added - New files appeared in directory; added to end of file
    for file in dir_files:
        if not dir_files:
            logger.info(f"Directory Added: {path}")

    # Files deleted - Previously watched and disappeared/Not changed
    if not dir_files:
        logger.info(f"Directory Not Found: {path}")

    # Files appended - Changed
    if not dir_files:
        logger.info(f"Directory Appended Files: {path}")


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

    """
    Add the arguments for dirwatcher
    The add_argument() method tells the ArgumentParser how to take the strings
    on the command line and turn them into objects. This information is stored
    and used when parse_args() is called.
    """
    parser.add_argument(
        "path", default=".",
        help="Specify the directory to watch",
        # Runs no matter the number of args input in the terminal
        nargs="?"
        )
    parser.add_argument(
        "magic", default="flow",
        help="Magic text to search for",
        # Runs no matter the number of args input in the terminal
        nargs="?"
        )
    parser.add_argument(
        "-e", "--extension", default=".txt",
        help="Filters type of file extension to search within",
        )
    parser.add_argument(
        "-i", "--interval", default="3",
        type=int, help="Polling interval",
        )
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

    # Exit strategy for long running program to gracefully shutdow; 
    # Signals have greater priority than the Exceptions and will execute first
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

    # Create start_up banner
    # File name that is running; Add time_stamp format
    start_time = datetime.datetime.now()
    start_up = (
        "\n" +
        "*" * 100 +
        f"\n\tRunning {__file__}" +
        f"\n\tStarted on {start_time.isoformat()}\n" +
        "*" * 100
    )
    # Issues a log message from the start_up strings
    logger.info(start_up)

    # global state_of_files

    while not exit_flag:
        try:
            # The code to be monitored by try clause to detect an exception
            # Call the watch_directory function - What's missing here??
            # watch_directory(args.path)
            logger.error(f"Does this work?")
            time.sleep(args.interval)
        # OSError is a built-in exception in Python and serves as the error
        # class for the os module, which is raised when an os specific system
        # function returns a system-related error, including I/O failures such
        # as “file not found” or “disk full”. --GeeksForGeeks
        except OSError as err:
            logger.error(f"Directory Not Found: {err}")
            time.sleep(args.interval)
        except KeyboardInterrupt as key:
            logger.error(f"Keyboard Command: {key}")
        except FileNotFoundError as err:
            # FileNotFoundError - [Errno 2] No such file or directory: dir1.txt
            logger.error(f"File Not Found: {err}")
        # Keep this except clause at the end to allow other exceptions to run
        except Exception as err:
            # This is an UNHANDLED exception - Log an ERROR level message here
            logger.error(f"Exception Message: {err}")
            # put a sleep inside my while loop so I don't peg the cpu usage
            # at 100%. EX: time.sleep(polling_interval)
            time.sleep(args.interval)

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

    # Informs the logging system to perform an orderly shutdown by flushing
    # and closing all handlers. This should be called at application exit and
    # no further use of the logging system should be made after this call.
    # logging.shutdown()


# Import guard clause
if __name__ == '__main__':
    main(sys.argv[1:])
