import argparse
import logging as log
import os

class UTRArgs:
	def __init__(self):
		self.parser = UTRArgs.create_parser()

	@staticmethod
	def create_parser():
		parser = argparse.ArgumentParser(description='Fetch and save the UTR ranking for a given player.')
		parser.add_argument('--username', type=str, default=os.getenv('UTR_USERNAME'), help='Player email/username')
		parser.add_argument('--password', type=str, default=os.getenv('UTR_PASSWORD'), help='Player password (will not save)')
		parser.add_argument('--output', type=str, default='utr_results.csv', help='Filename to append results (default: utr_results.csv)')
		parser.add_argument('-v', '--verbose', action="store_true", help='Verbose output')

		# Optionally, select a different player other than the one logged in
		group = parser.add_mutually_exclusive_group()
		group.add_argument('--id', type=int, help='Player ID (defaults to the player with matching username)')
		group.add_argument('--name', type=str, help='Player name (defaults to the player with matching username)')
		return parser

	def parse(self):
		args = self.parser.parse_args()
		if args.verbose:
			log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
			log.info("Verbose output")
		else:
			log.basicConfig(format="%(levelname)s: %(message)s")
		return args
