from matplotlib import dates, pyplot
import pandas as pd


def plot_utr_data(filename):
	df = pd.read_csv(filename, parse_dates=['timestamp'])
	ax = pyplot.axes()

	# Format line properties
	base_colors = pyplot.rcParams['axes.prop_cycle'].by_key()['color']
	ax.set_prop_cycle(color=[c for pair in zip(base_colors, base_colors) for c in pair])

	# Plot data
	for player_id in df.id.unique():
		player_df = df[df.id == player_id]
		player_name = player_df.displayName.iloc[0]
		ax.plot('timestamp', 'singlesUtr', data=player_df, label=player_name + " (Singles)")
		ax.plot('timestamp', 'doublesUtr', data=player_df, label=player_name + " (Doubles)", linestyle='dashed')

	# Format graph
	ax.set_xlabel('Date')
	ax.set_ylabel('UTR')
	ax.xaxis.set_major_locator(dates.MonthLocator(interval=3))
	ax.xaxis.set_minor_locator(dates.MonthLocator())
	ax.grid(True)
	ax.legend()

	# Display data
	pyplot.show()
