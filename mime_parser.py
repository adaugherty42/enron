import config
import email
import json
import os
import re

extra_char_regex = re.compile(r'[\.\,\;\:\'\"]+')
whitespace_regex = re.compile(r'[\s]+')
hyphen_regex = re.compile(r'[\-]+')


def parse_raw_data():
    root_dir = config.raw_email_dir()
    output_dir = config.json_email_dir()

    print('Parsing raw email data to json files...')

    for directory in os.listdir(root_dir):
        dir_path = os.path.join(root_dir, directory)
        file_list = traverse_dir(dir_path)
        with open(output_dir + '\\' + directory + '.json', 'w') as write_fp:
            json.dump(file_list, write_fp, indent=4)
        print(f'Finished directory {directory}')

    print('Finished parsing raw email data')


def traverse_dir(curr_path):
    file_list = []

    for path in os.listdir(curr_path):
        full_path = os.path.join(curr_path, path)
        if os.path.isdir(full_path):
            file_list.extend(traverse_dir(full_path))
        elif os.path.isfile(full_path):
            file_list.append(process_file(full_path))

    return file_list


def process_file(file_path):
    with open(file_path) as fp:
        email_message = email.message_from_string(fp.read())

        return {
            'from': email_message['From'],
            'to': email_message['To'],
            'cc': email_message['Cc'],
            'subject': email_message['Subject'],
            'body': clean_text(email_message.get_payload())
        }


def clean_text(text):
    extra_chars_removed = re.sub(extra_char_regex, ' ', text)
    extra_hyphens_removed = re.sub(hyphen_regex, '-', extra_chars_removed)
    return re.sub(whitespace_regex, ' ', extra_hyphens_removed)

