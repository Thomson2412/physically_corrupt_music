import os
import shutil
import hashlib


def clear(clear_dir):
    for root, dirs, files in os.walk(clear_dir):
        for filename in files:
            os.remove(os.path.join(root, filename))


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
            if os.path.isfile(new_filepath):
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
    input_files = "input"
    corrupted_dir = "corrupted"
    corrupted_dir_count = 0
    for root, dirs, files in os.walk(input_files):
        for filename in files:
            file = os.path.join(root, filename)
            clear(sdcard)
            fill(sdcard, file)
            corrupted_dir_count_path = os.path.join(corrupted_dir, str(corrupted_dir_count))
            while os.path.isdir(corrupted_dir_count_path) and not os.listdir(corrupted_dir_count_path):
                corrupted_dir_count = corrupted_dir_count + 1
                corrupted_dir_count_path = os.path.join(corrupted_dir, str(corrupted_dir_count))
            if not os.path.isdir(corrupted_dir_count_path):
                os.makedirs(corrupted_dir_count_path)
            corruption_check(sdcard, file, corrupted_dir_count_path)
