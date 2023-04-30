#!/usr/bin/python3

import argparse
import logging as log

from session import UTRSession
from filesystem import append_utr_data


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


if __name__ == '__main__':
	args = UTRArgs().parse()
	session = UTRSession().login(args.username, args.password)
	data = session.get_player_data(args.id, args.name)
	append_utr_data(args.output, data)
