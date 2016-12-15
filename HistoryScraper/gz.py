import gzip
with gzip.open('file.txt', 'rb') as f:
	file_content = f.read()
	print (file_content)
