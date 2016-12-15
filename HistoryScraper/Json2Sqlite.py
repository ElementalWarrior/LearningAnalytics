import ujson
import sqlite3
from unidecode import unidecode
import pdb
import sys

for arg in sys.argv:
	if arg.lower() == '--help':
		print ('json2sqlite.py <json input file> <sqlite output file>')
		sys.exit(0)

json_file = sys.argv[1]
sqlite_file = sys.argv[2]

data = ujson.loads(open(json_file, 'rb').read().decode('utf-8'), 'utf-8')
db = sqlite3.connect(sqlite_file)
c = db.cursor()
# pdb.set_trace()
cnt = c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = 'history'").fetchone()[0]
if cnt == 0:
	print('executed')
	c.execute('''
		create table history (
			url text,
			body text,
			title text,
			timestamp datetime
		)
	''')
	db.commit()
urls = ''
i = 0
for row in data:
	urls += row['url'] + '\n'
	if i % 10 == 0:
		print (urls)
		urls = ''
	c.execute("insert into history select ?,?,?,?", (
		  unidecode(row['url'])
		, unidecode(row['body'])
		, unidecode(row['title'])
		, unidecode(row['timestamp'])))
db.commit()
c.close()
