import os
import shutil
import hashlib


def clear(clear_dir):
    if os.listdir(clear_dir):
        shutil.rmtree(clear_dir)


def fill(input_dir, filepath):
    count = 0
    while True:
        try:
            filename_split = os.path.splitext(filepath)
            new_filename = f"{filename_split[0]}_{count}{filename_split[1]}"
            shutil.copy(filepath, os.path.join(input_dir, new_filename))
            count = count + 1
            print(f"Copied to: {new_filename}")
        except IOError:
            break


def corruption_check(input_dir, filepath_og, output_dir):
    md5_good = file_md5(filepath_og)
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            filepath_test = os.path.join(root, filename)
            md5_test = file_md5(filepath_test)
            if md5_good != md5_test:
                print(f"Corrupted: {filepath_test}")
                if output_dir is not None:
                    shutil.copy(filepath_test, output_dir)


def file_md5(filepath):
    with open(filepath, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()


if __name__ == '__main__':
    sdcard = "/media/thomas/169B-66A4"
    input_file = "input/Jan_Wolkers.mp3"
    corrupted_dir = "corrupted"
    # clear(sdcard)
    # fill(sdcard, input_file)
    # corruption_check(sdcard, input_file, corrupted_dir)
    corruption_check(sdcard, input_file, None)
