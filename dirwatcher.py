# !/usr/bin/env python3

"""
Dirwatcher - A long-running program to monitor directories and files for a
magic keyphrase taken from a command line argument. If the magic phrase is
found, a new message will be logged with the file and line number the text
was found.
"""

__author__ = """T.L. Williams(tlwilliams895)"""

import sys
import os
import argparse
import logging
import signal
import time
import datetime


logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)-8s %(lineno)d",
    datefmt="%A, %B %d, %Y--%I:%M:%S%p",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


"""Global Variables"""
exit_flag = False
watched_files = {}

def watch_directory(path, magic_string, extension, interval):
""""Watches a directory for given file/text combination"""
    global watched_files

    directory = os.path.isdir(path)
    list_dir = os.listdir(path)

    if not directory:
        logger.info(f"Directory Not Found: {path}")
    else:
        files = [file for file in list_dir if file.endswith(extension)]

        for file in files:
            if file not in watched_files:
                watched_files[file] = 0
                logger.info(f"New File: {file} was Found")
            new_file = os.path.join(path, file)

            """Searches through a file for magic text taken from CLI args"""
            with open(new_file) as f:
                lines_counted = watched_files[file]
                line_count = watched_files[file]
                lines = f.readlines()
                for index, line in enumerate(lines[line_count:]):
                    line_count += 1
                    if magic_string in line:
                        ending_line = index + lines_counted + 1
                        logger.info(f"Magic_Text: {magic_string}; File_Name: {file}; Line #{ending_line}") # noqa (no quality assurance)
                watched_files[file] = line_count
        """
        Delete the file containing the magic text — Dirwatcher should report
        the file as removed, only once.
        """
        del_files = []
        for file in watched_files:
            if file not in files:
                del_files.append(file)
                logger.info(f"File Deleted: {file}")
        for file in del_files:
            del watched_files[file]


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser(
        prog="DirWatcher",
        description="Program will continually search all files for modifications in directories.", # noqa
        epilog="Enjoy the DirWatcher program! :-)"
    )

    parser.add_argument("path", default=".",
                        help="Specify the directory to watch",
                        nargs="?")
    parser.add_argument("magic", default="flow",
                        help="Magic text to search for",
                        nargs="?")

    parser.add_argument("-i", "--interval", default="1",
                        type=int, help="Polling interval")
    """
    Argument that filters what kind of file extension to search within
    (i.e., .txt, .log)
    """
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
    """
    # log the associated signal name
    global exit_flag

    logger.warning('Signal Received: ' + signal.Signals(sig_num).name)

    exit_flag = True


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler() will get called if OS sends
    # either of these to my process.

    start_time = datetime.datetime.now()
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
            watch_directory(
                args.path,
                args.magic,
                args.extension,
                args.interval
            )
        except KeyboardInterrupt:
            break
        except FileNotFoundError:
            time.sleep(5)
            logger.error("Directory Does Not Exist")
        except RuntimeError as err:
            logger.error("Received and Logged Runtime Error: ", err)
        except Exception as err:
            logger.error("Unhandled Exception: ", err)

        # Add a sleep inside my while loop to prevent cpu usage at 100%
        time.sleep(args.interval)

    total_runtime = datetime.datetime.now() - start_time
    shut_down = (
        "\n" +
        "*" * 100 +
        f"\n\tStopped at: {__file__}" +
        f"\n\tTotal Runtime: {total_runtime}\n" +
        "*" * 100
    )
    logger.info(shut_down)


if __name__ == '__main__':
    main(sys.argv[1:])
