import csv
from Document import Document
from DocumentProfile import DocumentProfile
from PorterStemmer import PorterStemmer
import sys
import os
import pdb

stopfile = open(os.path.dirname(os.path.realpath(__file__)) + '\\stopwords.txt', 'r')
stemmer = PorterStemmer()
# print(dir(stemmer))
#build stop words array
stop_words = []
for line in stopfile:
	stop_words.append(line.replace('\n', ''))
def filter_non_alpha(data):
	i = 0
	while i < len(data):
		char = data[i]
		if char not in 'abcdefghijklmnopqrstuvwxyz ':
			data = data[0:i] + data[i+1:]
		else:
			i += 1
	return data
def strip_stop_words(data_arr):
	filtered = []
	for word in data_arr:
		is_stop_word = False
		for stop_word in stop_words:
			if word == stop_word:
				is_stop_word = True
				break
		if is_stop_word:
			continue
		else:
			filtered.append(word)
	return filtered
def stem_words(data_arr):
	for i in range(0, len(data_arr)):
		data_arr[i] = stemmer.stem_word(data_arr[i])
	return data_arr
def create_vector(data):
	data = filter_non_alpha(data.lower())
	data_arr = data.split()
	data_arr = strip_stop_words(data_arr)
	data_arr = stem_words(data_arr)

	vec = {}
	for word in data_arr:
		cnt = None
		if word not in vec:
			cnt = 0
		else:
			cnt = vec[word]
		vec[word] = cnt + 1
	return vec
def create_document_profile(file_path):
	with open(file_path, 'r') as csvfile:
		csv.field_size_limit(2**30)
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')
		is_first = True
		docs = []
		i = 0
		cols = None
		url_index = None
		post_time_index = None
		data_index = None
		author_index = None
		title_index = None
		for row in reader:
			if len(row) == 0:
				continue
			if i >= 200:
				break
			i = i + 1
			#skip the header row
			if is_first:
				cols = row
				url_index = cols.index('url')
				post_time_index = cols.index('post_time')
				data_index = cols.index('data')
				author_index = cols.index('author') if 'author' in cols else None
				title_index = cols.index('title') if 'title' in cols else None
				is_first = False
				continue
			# pdb.set_trace()
			url = row[url_index]
			post_time = row[post_time_index]

			#having issues with really long lines, lets truncate after something huge.
			data = row[data_index][:10000]
			author = None
			title = None
			if(author_index is not None):
				author = row[author_index]
			if(title_index is not None):
				title = row[title_index]
			word_vector = create_vector(data)
			if len(data) == 0:
				continue
			doc = Document(word_vector, url,post_time, data, author, title)
			docs.append(doc)
		return DocumentProfile(docs)
if __name__ == "__main__":
	if sys.argv[1] == "--help":
		print ('%s <document profile> <user profile>' % sys.argv[0])
		sys.exit(0)

	print('Loading Document Profile')
	doc_profile = create_document_profile(sys.argv[1])
	print('Loading User Profile')
	user_profile = create_document_profile(sys.argv[2])

	print('Computing most similar documents')
	most_similar_docs = []
	for doc in doc_profile.documents:
		cosine_sim = user_profile.profile.compare_document(doc)
		if len(most_similar_docs) == 0 or cosine_sim > most_similar_docs[len(most_similar_docs)-1]['cosine_sim']:
			most_similar_docs.append({'cosine_sim': cosine_sim, 'doc': doc})
			cosine_sim = sorted(most_similar_docs, key=lambda x: x['cosine_sim'])
			if len(most_similar_docs) > 5:
				most_similar_docs.pop(0)

	most_similar_docs.reverse()
	#print out similar docs
	for dic in most_similar_docs:
		print ('\n',dic['doc'].title)
		print (dic['doc'].url)
		print ('Cosine Similarity: %f\n' % dic['cosine_sim'])
