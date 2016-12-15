import copy
import math
from Document import Document
class DocumentProfile:
	def __init__(self, documents):
		self.documents = documents

		#inline cause we don't need to call this again
		def collection_of_word_counts():
			'''
				Go through each document and create a dictionary to cound the number
				of documents each word is in
			'''
			dict = {}
			for doc in documents:
				for word in doc.word_vector.keys():
					if word in dict:
						dict[word] = dict[word] + 1
					else:
						dict[word] = 1
			return dict

		self.word_instances = collection_of_word_counts()
		self.profile = {}
		for doc in documents:
			new_word_vector = copy.deepcopy(doc.word_vector)
			for word in new_word_vector.keys():
				new_word_vector[word] = doc.term_frequency(word) * self.inverse_document_frequency(word)
				if word not in self.profile:
					self.profile[word] = 0
				self.profile[word] += new_word_vector[word]
		self.profile = Document(word_vector = self.profile)
	def inverse_document_frequency(self, word):
		return math.log10(len(self.documents)/self.word_instances[word])
