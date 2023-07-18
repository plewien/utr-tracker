#!/usr/bin/python3

from config import UTRArgs
from session import UTRSession

if __name__ == '__main__':
	args = UTRArgs().parse()

	if args.save:
		from filesystem import append_utr_data
		session = UTRSession().login(args.username, args.password)
		data = session.get_player_data(args.id, args.name)
		append_utr_data(args.database, data)

	if args.graph:
		from graph import plot_utr_data
		plot_utr_data(args.database)
