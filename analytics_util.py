#! /usr/bin/env python

import datetime
from dateutil.parser import parse
import gzip
import json
import re

def chunks(arr, chunk_size):
  for i in xrange(0, len(arr), chunk_size):
    yield arr[i:i+chunk_size]

def date_range_gen(start_date, end_date):
  for n in range(int((end_date - start_date).days)):
    yield start_date + datetime.timedelta(n)

def filter_event(event, keywords):
  for keyword in keywords:
    if keyword in event:
      return True
  return False

def load_time_sorted_event(event_filename, keywords, filtered_function=lambda x: False):
  events = []
  for line in open(event_filename):
    if not filter_event(line, keywords):
      continue
    event = json.loads(line)
    if filtered_function(event):
      continue
    events.append(event)
  return sorted(events, key=lambda x:parse(x['time']))

def load_csv_like(filename, delimiter):
  header = None
  for line in open(filename):
    if header:
      yield (header, re.split(delimiter, line.strip()))
    else:
      header = re.split(delimiter, line.strip())

def load_users(user_list):
  with open(user_list) as f:
    return [int(re.split('\t', line.strip())[0]) for line in f.readlines()]

def time_diff(start_time, end_time):
  return (parse(end_time)-parse(start_time)).total_seconds()
