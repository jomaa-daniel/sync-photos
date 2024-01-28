#!/usr/bin/env python3
import os
import sys
import _stat
import shutil
from datetime import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#### EDIT THESE ######
SOURCE_PATH = "/mnt/e/DCIM/100CANON"
TARGET_PATH = "/mnt/c/Users/Daniel Jomaa/OneDrive/Camera/TODO/all-pictures"
DEBUG = True
REMOVABLE_DRIVE_NAME = "E"
REMOVABLE_DRIVE_PATH = "/mnt/" + REMOVABLE_DRIVE_NAME.lower()


def get_files_list(path):
    normalized_path = os.path.normpath(path)
    try:
        os.chmod(path, _stat.S_IWRITE)
        os.chmod(path, _stat.S_IREAD)
    except BaseException as e:
        if DEBUG:
            print(bcolors.FAIL + "DEBUG: " + str(e) + bcolors.ENDC)
        print("There was an issue connecting to the source directory: ", normalized_path)
        exit(1)

    # check if the source folder is accessible and readable
    file_list = []
    try:
        file_list = os.listdir(normalized_path)
    except BaseException as e:
        if DEBUG:
            print(bcolors.FAIL + "DEBUG: " + str(e) + bcolors.ENDC)
        print("There was an issue reading the source directory")
        exit(1)
    return file_list


def find_new_pictures(source_pictures, target_pictures):
    target_pictures_set = set(target_pictures)
    new_pictures = []
    for source_picture in source_pictures:
        if source_picture not in target_pictures_set:
            new_pictures.append(source_picture)
    return new_pictures


def log(new_log, log_file):
    log_file.write(f"[{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}] {new_log} \n")


def copy_pictures(new_pictures, log_file):
    wrote_files = 0
    try:
        for new_picture in new_pictures:
            source_path = f"{SOURCE_PATH}/{new_picture}"
            target_path = f"{TARGET_PATH}/{new_picture}"
            msg = f"Copying {source_path} to {target_path}"
            print(msg)
            shutil.copy2(source_path, target_path)
            wrote_files += 1
            log(msg, log_file)
    except BaseException as e:
        err_msg = f"Wrote {wrote_files} before Encountering Error: {str(e)}"
        print(err_msg)
        log(err_msg, log_file)
    success_msg = f"Wrote all {wrote_files} files"
    print(success_msg)
    log(success_msg, log_file)


def main():
    # mount the drive
    cmd = f"sudo mount -t drvfs {REMOVABLE_DRIVE_NAME}: {REMOVABLE_DRIVE_PATH}"
    print(f"Mounting drive {REMOVABLE_DRIVE_NAME} at location {REMOVABLE_DRIVE_PATH}")
    code = os.system(cmd)
    if code != 0:
        print(f'There was an issue mounting the drive: {REMOVABLE_DRIVE_PATH}')
        exit(1)

    # check if the target folder exists
    source_file_list = get_files_list(SOURCE_PATH)
    target_file_list = get_files_list(TARGET_PATH)
    # check if the target folder is accessible
    new_pictures = find_new_pictures(source_pictures=source_file_list, target_pictures=target_file_list)
    print(f"{datetime.now()} Found {len(new_pictures)} new pictures, copying...")
    log_file = open(f"{os.getcwd()}/[{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}] - logs.txt", "a")
    log(f"Copying {len(new_pictures)} pictures...\n", log_file)
    copy_pictures(new_pictures, log_file)
    log_file.close()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
