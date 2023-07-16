To use:
- Download enron dataset from https://www.cs.cmu.edu/~enron/
- Set up directories in config.py.
  - raw_email_dir is the directory you extract the dataset to.
  - json_email_dir is the directory the cleaned/simplified json emails will be written to
  - tf_idf_output_dir is the directory the tf-idf results will be written to, since the emails can be quite large and difficult to read in a terminal
- Run `python enron.py --parse` once to parse the raw emails. This will take a while.
- Run `python enron.py --tf-idf "your search query here"` to run tf-idf on a search query.
