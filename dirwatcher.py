# !/usr/bin/env python3

"""
Dirwatcher - A long-running program to monitor directories and files for a
magic keyphrase taken from a command line argument. If the magic phrase is
found, a new message will be logged with the file and line number the text
was found.
"""

__author__ = """T.L. Williams(tlwilliams895) completed assessment with
        Deidre Boddie and Dessance Chandler; used Python docs, RealPython
        website, SE workshop/demos, and other resources to complete assessment
        Received assistance from Kano Marvel, JT Maupin, and Mike Boring
        """

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

exit_flag = False
watched_files = {}

def watch_directory(path, magic_string, extension, interval):
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

            with open(new_file) as f:
                lines_counted = watched_files[file]
                line_count = watched_files[file]
                lines = f.readlines()
                for index, line in enumerate(lines[line_count:]):
                    line_count += 1
                    if magic_string in line:
                        ending_line = index + lines_counted + 1
                        logger.info(
                            f"Magic_Text: {magic_string}; Found in file: {file}; Line #{ending_line}"
                            )
                watched_files[file] = line_count

        del_files = []
        for file in watched_files:
            if file not in files:
                del_files.append(file)
                logger.info(f"File Deleted: {file}")
        for file in del_files:
            del watched_files[file]


def create_parser():
    parser = argparse.ArgumentParser(
        prog="DirWatcher",
        description="Program will continually search within all files for modifications in the directory.",
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

    parser.add_argument("-e", "--extension", default=".txt",
                        help="Filters type of file extension to search within")
    return parser


def signal_handler(sig_num, frame):
    global exit_flag

    logger.warning('Signal Received: ' + signal.Signals(sig_num).name)

    exit_flag = True


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

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
            logger.error("File Not Found")
        except RuntimeError as err:
            logger.error("Received and Logged Runtime Error: ", err)
        except Exception as err:
            logger.error("Exception Message: ", err)
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
