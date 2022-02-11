import os
import shutil
import hashlib


def clear(clear_dir):
    if os.listdir(clear_dir):
        shutil.rmtree(clear_dir)


def fill(input_dir, filepath):
    count = 0
    while True:
        filename_split = os.path.splitext(os.path.basename(filepath))
        new_filename = f"{filename_split[0]}_{count}{filename_split[1]}"
        new_filepath = os.path.join(input_dir, new_filename)
        try:
            shutil.copy(filepath, new_filepath)
            count = count + 1
        except IOError:
            os.remove(new_filepath)
            break
        print(f"Copied to: {new_filepath}")


def corruption_check(input_dir, filepath_og, output_dir):
    corrupted_count = 0
    md5_good = file_md5(filepath_og)
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            filepath_test = os.path.join(root, filename)
            md5_test = file_md5(filepath_test)
            if md5_good != md5_test:
                print(f"Corrupted: {filepath_test}")
                corrupted_count = corrupted_count + 1
                if output_dir is not None:
                    shutil.copy(filepath_test, output_dir)
            else:
                print(f"Good: {filepath_test}")
    print(f"Amount Corrupted: {corrupted_count}")


def file_md5(filepath):
    with open(filepath, 'rb') as file:
        return hashlib.md5(file.read()).hexdigest()


if __name__ == '__main__':
    sdcard = "/media/thomas/169B-66A4"
    input_file = "input/BAF-BREIN.mp3"
    corrupted_dir = "corrupted"
    clear(sdcard)
    fill(sdcard, input_file)
    # corruption_check(sdcard, input_file, corrupted_dir)
    corruption_check(sdcard, input_file, None)
