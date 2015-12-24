#! /usr/bin/env python

def load_csv_like(filename, delimiter):
  header = None
  for line in open(filename):
    if header:
      yield (header, re.split(delimiter, line.strip()))
    else:
      header = re.split(delimiter, line.strip())

