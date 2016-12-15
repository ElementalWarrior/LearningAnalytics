import math
import pdb
# import pdb
class Document:
	def __init__(self, word_vector, url = None, post_time = None, data = None, author = None, title = None):
		if url is not None:
			self.url = url
		if post_time is not None:
			self.post_time = post_time
		if data is not None:
			self.data = data
		if author is not None:
			self.author = author
		if title is not None:
			self.title = title
		self.word_vector = word_vector
	def total_words(self):
		cnt = 0
		for word in self.word_vector.keys():
			cnt += self.word_vector[word]
		return cnt
	def term_frequency(self, word):
		if word not in self.word_vector.keys():
			return 0
		return self.word_vector[word]
	def magnitude(self):
		mag = 0
		# pdb.set_trace()
		for word in self.word_vector.keys():
			mag = mag + math.pow(self.word_vector[word], 2)
		mag = math.sqrt(mag)
		return mag
	def compare_document(self, doc):
		dot_prod = 0
		handled_words = []
		for word in self.word_vector.keys():
			handled_words.append(word)
			dot_prod = dot_prod + self.word_vector[word] * (doc.word_vector[word] if word in doc.word_vector.keys() else 0)
		for word in doc.word_vector.keys():
			if word in handled_words:
				continue
			handled_words.append(word)
			dot_prod = dot_prod + doc.word_vector[word] * (self.word_vector[word] if word in self.word_vector.keys() else 0)
		if(self.magnitude() == 0 or doc.magnitude() == 0):
			return 0
		return dot_prod/(self.magnitude() * doc.magnitude())
