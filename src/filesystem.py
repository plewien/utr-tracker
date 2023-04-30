import csv
from datetime import datetime
import logging as log
import os

def merge_no_duplicates(list1, list2):
	result = list(list1) if list1 else []
	result.extend(x for x in list2 if x not in result)
	return result

def select_keys(data, keys):
	return { key: data[key] for key in keys }

def same_fields_in_csv_file(filename, fields):
	with open(filename, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		return fields == reader.fieldnames

def read_csv(filename):
	with open(filename, 'r+') as csvfile:
		reader = csv.DictReader(csvfile)
		data = list(reader)
		keys = reader.fieldnames
	return data, keys

def append_csv(filename, row, keys):
	with open(filename, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=keys)
		writer.writerow(row)

def write_csv(filename, data, keys):
	with open(filename, 'w+') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=keys)
		writer.writeheader()
		writer.writerows(data)

def append_utr_data(filename, newdata):
	newdata['timestamp'] = datetime.now()
	keys = ['timestamp', 'id', 'displayName', 'singlesUtr', 'doublesUtr']
	if not os.path.exists(filename):
		log.debug('Making new output file')
		write_csv(filename, [select_keys(newdata, keys)], keys)
	elif same_fields_in_csv_file(filename, keys):
		log.debug('Same fields found in output file, appending new data')
		append_csv(filename, select_keys(newdata, keys), keys)
	else:
		log.debug('New fields added, rewriting output file')
		data, current_keys = read_csv(filename)
		keys = merge_no_duplicates(current_keys, keys)
		data.append(select_keys(newdata, keys))
		write_csv(filename, data, keys)
