import argparse
import sqlite3
import datetime
import csv
import pdb
import random

parser = argparse.ArgumentParser(description = "Generate a user profile based on a sqlite file.")
parser.add_argument('sqlite', metavar = 'sqlite', type=str, help='Path to your sqlite file.')
parser.add_argument('output', metavar = 'output', type=str, help='Path to your ourput file.')
parser.add_argument('--timestamp', '-t', dest="timestamp", type=str, default=None, help='Maximum date to return up until.')
parser.add_argument('--time_format', '-f', dest="format", type=str, default="%Y-%m-%dT%H:%M:%SZ", help='Format of time to use. Reference Here https://docs.python.org/3/library/time.html#time.strptime')
parser.add_argument('-k, --keywords', dest="keywords", metavar = 'k', type=str, default=None, help='Only return pages that contain at least one of the supplied keywords.')

args = parser.parse_args()

#setup vars from args
conn = sqlite3.connect(args.sqlite)
timestamp = None
keywords = None
if args.timestamp is not None:
	timestamp = datetime.datetime.strptime(args.timestamp.translate({ord(':'): None, ord('-'): None})
										, args.format.translate({ord(':'): None, ord('-'): None}))
if args.keywords is not None:
	keywords = args.keywords.split()

c = conn.cursor()

#get column positions
cols = []
for row in c.execute("PRAGMA table_info('history')").fetchall():
	cols.append(row[1])


#if timestamp provided let sqlite filter by time
results = []
if timestamp is None:
	results = c.execute('select url, body, title, timestamp from history').fetchall()
else:
	results = c.execute('select url, body, title, timestamp from history where timestamp <= ?', (timestamp,)).fetchall()

#if we supplied keywords we have to filter the results
if keywords is not None:
	res = []
	for row in results:
		#check if page includes our keywords
		for word in keywords:
			if word.lower() in row[cols.index('body')].lower():
				res.append(row)
				#break out of keyword loop cause we have a hit
				break

	results = res


#use a random sample if we have enough results
if len(results) > 200:
	results = sorted(random.sample(results, int(len(results)*0.7)))
with open(args.output, 'w') as out:
	writer = csv.writer(out, delimiter = ',', quotechar = "\"", lineterminator = "\n")
	writer.writerow(['url', 'post_time', 'data'])
	for row in results:
		data = row[cols.index('body')]
		data = data.translate({
			ord('\n'): None,
			ord('\r'): None,
		})
		writer.writerow([row[cols.index('url')], row[cols.index('timestamp')], data.strip()])
