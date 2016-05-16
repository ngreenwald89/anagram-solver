import hashlib
import itertools
import operator
from timeit import default_timer as timer

anagram = "poultry outwits ants"
# sorted_anagram = sorted(anagram)
sorted_anagram = ['a', 'i', 'l', 'n', 'o', 'o', 'p', 'r', 's', 's', 't', 't', 't', 't', 'u', 'u', 'w', 'y']
md5hash = "4624d200580677270a54ccff86b9610e"

def try_open(filename):
	results = []
	with open(filename) as fp:
		wordlist = fp.readlines()
	for word in wordlist:
		word = word.split()[0]
		results.append(word)
	return results


def wordlist_subset(wordlist):	
	i = 0
	subset = []
	wordlist_length = len(wordlist)
	for word in wordlist:
		if sorted(word) == sorted_anagram:
			result = is_secret_code(word)
			if result:
				return result
		elif contains_all(word) == True:
			subset.append(word)
	return subset

# checks to see if a sorted word is a subset of the sorted_anagram
def contains_all(sword):
	sorted_anagram = ['a', 'i', 'l', 'n', 'o', 'o', 'p', 'r', 's', 's', 't', 't', 't', 't', 'u', 'u', 'w', 'y']
	for char in sword:
		if char not in sorted_anagram:
			return False
		else:
			sorted_anagram.remove(char)
	return True

def new_run(filename):
	start = timer()
	print('start', start)
	# open dictionary
	wordlist = try_open(filename)
	# see if any words in dictionary are 1. the anagram or 2. a subset of the anagram;
	subset = wordlist_subset(wordlist)
	return toms_way(subset)

def test_run(filename):
	start = timer()
	print('start', start)
	# open dictionary
	wordlist = try_open(filename)
	# see if any words in dictionary are 1. the anagram or 2. a subset of the anagram;
	subset = wordlist_subset(wordlist)
	# check if two word combinations are 1. the anagram or 2. a subset of the anagram
	# return combinations that are subset and the words subset that make up valid combinations
	combinations_subset, subset_dict = make_combinations(subset)
	# sort subset by the number of times a word occurred in a combination; try those words first
	sorted_subset = sorted(subset_dict.items(), key=operator.itemgetter(1))
	# get just the words, not the count
	new_subset = [t[0] for t in sorted_subset]

	return make_triples(subset=new_subset, combinations=combinations_subset)

def make_combinations(subset):
	# for word in subset:
	# 	for itertools.product([word], subset):
	combinations_subset = []
	subset_dict = {}
	count = 0
	for combination in itertools.combinations(subset, r=2):
		word1, word2 = combination
		sorted_combination = sorted(itertools.chain(*combination))
		if contains_all(sorted_combination):
			if word1 in subset_dict:
				subset_dict[word1] += -1
			else:
				subset_dict[word1] = -1
			if word2 in subset_dict:
				subset_dict[word2] += -1
			else:
				subset_dict[word2] = -1
			combinations_subset.append(combination)
		count += 1
		if count % 300000 == 0: print('two word combinations', count)
	return (combinations_subset, subset_dict)

def tom_sort(item):
	return item[2]

def make_triples(subset, combinations):
	count = 0
	for product in product_size(subset, combinations):
		count += 1
		# unchained = itertools.chain.from_iterable(product)
		# input(unchained)
		thing = itertools.chain(item if type(item) == str else ''.join(item) for item in product)
		sorted_product = sorted(itertools.chain(*thing))
		# print('past product_size')
		# input(sorted_product)
		if count % 10000 == 0: print("inside len match", count)
		if sorted_product == sorted_anagram:
			result = is_secret_code([product[0],*product[1]])
			if result:
				end = timer()
				print('end', end)
				return result



def product_size(subset, combinations):
	match_len = len(sorted_anagram)
	count = 0
	for product in itertools.product(subset, combinations):
		count += 1
		if count % 5000000 == 0: print("inside len check with subset and combinations", count)
		if match_len == sum(len(s) for s in itertools.chain(*product)):
			yield product

def combo_size(subset, r):
	match_len = len(sorted_anagram)
	for combination in itertools.combinations(subset, r=r):
		if match_len == sum(len(s) for s in combination):
			yield combination

def toms_way(subset):
	print('in toms way')
	count = 0
	# for combination in itertools.combinations(subset, r=3):
	for combination in combo_size(subset, 3):
		count += 1
		# if match_len != sum(len(s) for s in combination):
		# 	continue
		sorted_combination = sorted(itertools.chain(*combination))
		if count % 1000000 == 0: print(count)
		if sorted_combination == sorted_anagram:
			result = is_secret_code(combination)
			if result:
				end = timer()
				print('end', end)
				return result

# combo is anagram, now see if any permutation of combo is secret_code
def is_secret_code(combo):
	for permutation in itertools.permutations(combo):
		string = ' '.join(permutation)
		if hashlib.md5(string.encode("utf-8")).hexdigest() == md5hash:
			print('IS SECRET CODE!!', string)
			return string
	return False
