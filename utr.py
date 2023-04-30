#!/usr/bin/python3

import argparse
import csv
from datetime import datetime
import logging as log
import os
import requests


class UTRArgs:
	def __init__(self):
		self.parser = UTRArgs.create_parser()

	@staticmethod
	def create_parser():
		parser = argparse.ArgumentParser(description='Fetch and save the UTR ranking for a given player.')
		parser.add_argument('--username', type=str, help='Player username (email)')
		parser.add_argument('--password', type=str, help='Player password (will not save)')
		group = parser.add_mutually_exclusive_group()
		group.add_argument('--id', type=int, help='Player ID (check the url for your profile on https://app.universaltennis.com/)')
		group.add_argument('--name', type=str, help='Player name, specify to query database for the Player ID')
		parser.add_argument('--output', type=str, default='utr_results.csv', help='Filename to append results (default: utr_results.csv)')
		parser.add_argument('-v', '--verbose', action="store_true", help='Verbose output')
		return parser

	def parse(self):
		args = self.parser.parse_args()
		if args.verbose:
			log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
			log.info("Verbose output")
		else:
			log.basicConfig(format="%(levelname)s: %(message)s")
		return args


class Session:
	def __init__(self, url):
		self.session = requests.Session()
		self.url = url

	def safe_get(self, uri):
		with self.session.get(self.url + uri) as response:
			if (not response.ok):
				raise response.raise_for_status()
			return response.json()

	def safe_post(self, url, uri, headers=None, body=None):
		with self.session.post(url + uri, headers=headers, json=body) as response:
			if (not response.ok):
				raise response.raise_for_status()
			return response.json()


class UTRSession(Session):
	api_version='v1'
	def __init__(self):
		super().__init__('https://api.universaltennis.com')
		self.app_url = 'https://app.universaltennis.com/api'

	def login(self, username, password):
		uri = f'/{self.api_version}/auth/login'
		headers = {'Content-Type': 'application/json'}
		body = {'email' : username, 'password' : password}
		self.safe_post(self.app_url, uri, headers, body)
		log.debug(f'Successful login for {username}')
		return self

	def find_id(self, name):
		query = f'query={name}'
		data = self.safe_get(f'/{self.api_version}/search/players?top=1&{query}')
		if data['total'] == 0:
			raise Exception(f'Unable to find player ID for {name}: Zero results')
		elif data['total'] > 1:
			log.warning(f"{data['total']} players found with the same name")

		return data['hits'][0]['id']

	def get_profile_data(self, id):
		data = self.safe_get(f'/v1/player/{id}/profile')
		log.debug(f'Profile data: {data}')
		return data

	def get_player_data(self, id, name=None):
		if not id and not name:
			raise Exception("Must specify either a player name or id")
		elif not id:
			id = self.find_id(name)

		log.info(f"Searching stats for id {id}...")
		data = self.safe_get(f'/{self.api_version}/player/{id}/profile')

		log.info("Player found: {} with UTR {}/{} in {} {}, {}".format( \
				data['displayName'], data['singlesUtr'], data['doublesUtr'], \
				data['location']['cityName'], data['location']['stateAbbr'], data['location']['countryName']))
		return data


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


if __name__ == '__main__':
	args = UTRArgs().parse()
	session = UTRSession().login(args.username, args.password)
	data = session.get_player_data(args.id, args.name)
	append_utr_data(args.output, data)
