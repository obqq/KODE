import re
from itertools import combinations


def lev(s1: str, s2: str) -> int:
	'''
	Levenshtein distance
	https://en.wikipedia.org/wiki/Levenshtein_distance
	'''
	n = len(s1) + 1
	m = len(s2) + 1
	d = [[i if j == 0 else (j if i == 0 else 0) for j in range(m)] for i in range(n)]

	for i in range(1, n):
		for j in range(1, m):
			if s1[i - 1] == s2[j - 1]:
				indicator = 0
			else:
				indicator = 1

			d[i][j] = min(d[i - 1][j] + 1,
						  d[i][j - 1] + 1,
						  d[i - 1][j - 1] + indicator)

	return d[n - 1][m - 1]


def fuzzy_search(phrase: str, search_string: str, threshhold: float = 0.9) -> bool:
	'''
	Tells if :phrase: and :seacrh_string: are similar enough
	with respect to :threshhold: value.
	'''
	ld = lev(phrase, search_string)
	similarity = 1 - ld / max(len(phrase), len(search_string))

	if similarity > threshhold:
		return True
	else:
		return False


def find_keywords(phrase: str) -> list:
	'''
	Extracts keywords from the fields in a format string
	e.g. given "I wanna {eat} and {drink}" returns ['eat', 'drink']
	'''
	return re.findall('{(.*?)}', phrase)


def phrase_search(object_list: list, search_string: str, fuzzy=True) -> int:

	for object in object_list:
		phrase = object['phrase']
		values = object['slots']
		_id = object['id']

		keywords = find_keywords(phrase)
		combs = combinations(values, len(keywords))

		for comb in combs:
			args = dict(zip(keywords, comb))
			formatted_phrase = phrase.format(**args)

			if fuzzy:
				if fuzzy_search(formatted_phrase, search_string):
					return _id
			else:
				if formatted_phrase == search_string:
					return _id

	return 0


if __name__ == "__main__":
	"""
	len(object) != 0
	object["id"] > 0
	0 <= len(object["phrase"]) <= 120
	0 <= len(object["slots"]) <= 50
	"""
	object = [
		{"id": 1, "phrase": "Hello world!", "slots": []},
		{"id": 2, "phrase": "I wanna {pizza}", "slots": ["pizza", "BBQ", "pasta"]},
		{"id": 3, "phrase": "Give me your power", "slots": ["money", "gun"]},

		{"id": 4, "phrase": "I wanna {eat} and {drink}", "slots": ["pizza", "BBQ", "pepsi", "tea"]}
	]

	assert fuzzy_search('I wanna pizza', 'i wanna pizza') is True
	assert fuzzy_search('I wanna pizza', 'I wonna pizza') is True
	assert fuzzy_search('I wanna pizza', 'I wana pizza') is True
	assert fuzzy_search('I wanna pizza', 'I wanna pasta') is False
	assert fuzzy_search('I wanna pizza', 'I wanna BBQ') is False
	assert fuzzy_search('Give me your power', 'Give me your powers') is True
	assert fuzzy_search('Give me your power', 'Give me your gun') is False
	assert fuzzy_search('I wanna pizza and tea', 'I wanna pasta and tea') is False

	assert phrase_search(object, 'I wanna pasta') == 2
	assert phrase_search(object, 'Give me your power') == 3
	assert phrase_search(object, 'Hello world!') == 1
	assert phrase_search(object, 'I wanna nothing') == 0
	assert phrase_search(object, 'Hello again world!') == 0
	assert phrase_search(object, 'I need your clothes, your boots & your motorcycle') == 0

	assert phrase_search(object, 'I wanna pizza and pepsi') == 4
	assert phrase_search(object, 'I wanna pasta and tea') == 0
