import argparse
import config
import json
import os
import mime_parser
import tfidf


def main():
    arg_parser = argparse.ArgumentParser(
        prog='enron.py',
        description='Performs analysis on Enron dataset'
    )
    arg_parser.add_argument('--parse', '-p', action='store_true', default=False)
    arg_parser.add_argument('--tf-idf', action='store', default=None)

    args = arg_parser.parse_args()

    if args.parse:
        mime_parser.parse_raw_data()
    elif args.tf_idf:
        all_emails = load_emails()
        documents = tfidf.initialize_documents(all_emails, args.tf_idf)
        res = tfidf.calculate_top_search_results(documents, args.tf_idf)

        output_dir = config.tf_idf_output_dir()

        with open(output_dir + f'\\{args.tf_idf}.txt', 'w') as fp:
            for score, _, document in res:
                fp.write(f'Score: {score}, document: {document}\n\n')
                # print(f'Score: {score}, document: {document}')


def load_emails():
    print('Loading email json...')

    all_emails = []
    input_dir = config.json_email_dir()

    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        with open(file_path) as fp:
            emails = json.load(fp)
            all_emails.extend(emails)

    print('Finished loading email json')
    return all_emails


if __name__ == '__main__':
    main()
