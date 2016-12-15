import json
import csv

j = open('data.json')
data = json.load(j)
j.close()

c = csv.writer(open('data.csv', 'wb+'))
c.writerow(['url', 'title', 'data', 'author', 'post_time'])
for row in data:
	c.writerow([
		row['url']
		, row['title'].encode('utf-8').strip()
		, row['data'].encode('utf-8').strip()
		, row['author']
		, row['post_time']])
