# source logan/grading_tools
# Copyright 2020 Logan Gilmour
# Modified by Xinlei Chen
# Modified by Paul Lu
#	Significant changes hacked for GitHub classroom.  TODO More cleanup.


import os
# import zipfile
# import tarfile
# import shutil
# from tempfile import gettempdir
# from random import randint
from contextlib import contextmanager
import argparse

conf = {
    "submission_name": "ooclassifier",
    "specified_files": ["ooclassifier/ooclassifier.py", "ooclassifier/ooclassifierbase.py", "ooclassifier/README", "ooclassifier/Makefile", "ooclassifier/submission_validator.py", "ooclassifier/a1.task.1.unittest.v01.py", "ooclassifier/a1.task.2.unittest.v01.py", "ooclassifier/a1.task.3.unittest.v01.py", "ooclassifier/a1.alltasks.v01.py", "ooclassifier/a1.alltasks.v02.py"],
    "assignment_version": "Assignment #1 (2022)",
}

class ValidationException(Exception):
    pass


def get_contents(path):
    names = []
    for root, subFolder, files in os.walk(path):
        # names = []
        for name in files:
            subdir = os.path.relpath(root, path)
            if subdir != ".":
                names.append(os.path.join(subdir, name))
            else:
                names.append(name)
    return names


def validate_contents(archive_filename, extracted_dir, specified_files):
    all_files = get_contents(extracted_dir)
    # found_files = get_contents(extracted_dir)
    # Delete git and similar files
    found_files = []
    for f in all_files:
        if ".git" in f:
            continue
        if ".DS_Store" in f:
            continue
        if "__pycache__" in f:
            continue
        if ".swp" in f:
            continue
        if "Tests" in f:
            continue
        if "Expected" in f:
            continue
        if "Demo" in f:
            continue
        found_files.append(f)

    if set(found_files) != set(specified_files):
    # if not set(specified_files).issubset(set(found_files)):
        raise ValidationException("{} should contain exactly:\n{}\n\nbut instead contains:\n{}"
                                      .format(archive_filename, "\n".join(specified_files), "\n".join(found_files)))


def extract_submission(submission_name, extracted_dir):
    # Paul Lu:  Simplified placeholder
    archive_filename = ""
    extracted_dir = ".."

    return archive_filename, extracted_dir


@contextmanager
def extract_submission_temp(submission_name):
    # Paul Lu:  Simplified placeholder
    extracted_dir = ""

    yield extract_submission(submission_name, extracted_dir)



def validate_submission():
    print("=== CMPUT 274 {} Validator ===".format(conf["assignment_version"]))

    try:
        with extract_submission_temp(conf["submission_name"]) as (archive_filename, extracted_dir):
            # print("Successfully extracted {}".format(archive_filename))

            validate_contents(archive_filename, extracted_dir, conf["specified_files"])
            print("File structure appears to be correct.")

            print("\nVALIDATION SUCCEEDED.")
            print("\nDISCLAIMER: This does not mean that your submission is correct "
                  "- just that it appears to be structured correctly.")
            print("\n** Best run this on a fresh clone of your repository.")

    except ValidationException as e:
        print("\nVALIDATION FAILED")
        print(e)
        print("Please fix this and try validating again.")
    except Exception as e:
        print("\nVALIDATION FAILED")
        print("Exception occurred: {}".format(e))
        print("Stopping validation. Please fix this and try again.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    description='''This script helps you to verify that your submission structure is correct for {}.
Usage:
  1. Place this file in the same directory as your Makefile
  2. Run the program using:
        python3 submission_validator.py
  3. The verification results will be shown.
      - If you see "VALIDATION SUCCEEDED", your submission appears to be
        structured correctly.
      - Otherwise, if you see "VALIDATION FAILED", you should examine the
        error message, fix the problem, and try again.
                                '''.format(conf["assignment_version"], conf["submission_name"], conf["submission_name"], conf["submission_name"]),
                                formatter_class = argparse.RawTextHelpFormatter

                    )
    args = parser.parse_args()

    validate_submission()
