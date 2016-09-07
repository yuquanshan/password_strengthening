#!/usr/bin/python

# gram-1 markov stats for each of the patterns
# 	L: lowercase letter
#	U: uppercase letter
# 	D: digit
# 	S: symbol
# usage: make_markov.py <passwords_file>

import sys,os
# all possible password characters
characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digit = "0123456789"
symbol = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

def getPattern(psswd):
	length = len(psswd)
	pattern = ""
	head = ""
	counter = 0
	for i in range(0,length):
		if psswd[i] in lowercase:
			if head == "L":
				counter = counter+1
			else:
				if head != "":
					pattern = pattern+head+str(counter)
				head = "L"
				counter = 1
		elif psswd[i] in uppercase:
			if head == "U":
				counter = counter+1
			else:
				if head != "":
					pattern = pattern+head+str(counter)
				head = "U"
				counter = 1 
		elif psswd[i] in digit:
			if head == "D":
				counter = counter+1
			else:
				if head != "":
					pattern = pattern+head+str(counter)
				head = "D"
				counter = 1
		else:
			if head == "S":
				counter = counter+1
			else:
				if head != "":
					pattern = pattern+head+str(counter)
				head = "S"
				counter = 1
		if(i==length-1):
			pattern = pattern+head+str(counter)
	return pattern

def main(filename):
	fi = file(filename,'r')
	lines = fi.readlines()
	output = file(filename+'.gram1mc','w')
	output.write("possible characters: "+characters+'\n')
	# study the pattern of each password in the password database
	pattern_lib = {}	# record patterns occurence
	lower_occurence = {}	#{length:{psswd:occurence}}
	upper_occurence = {}	
	digit_occurence = {}
	symbol_occurence = {}
	lower_markov = {}
	lower_firsthit = {}
	for i in lowercase:
		lower_markov[i] = [0]*len(lowercase)
		lower_firsthit[i] = 0
	upper_markov = {}
	upper_firsthit = {}
	for i in uppercase:
		upper_markov[i] = [0]*len(uppercase)
		upper_firsthit[i] = 0
	digit_markov = {}
	digit_firsthit = {}
	for i in digit:
		digit_markov[i] = [0]*len(digit)
		digit_firsthit[i] = 0
	symbol_markov = {}
	symbol_firsthit = {}
	for i in symbol:
		symbol_markov[i] = [0]*len(symbol)
		symbol_firsthit[i] = 0
	for l in lines:
		psswd = l.split()[0];
		pattern = getPattern(psswd)
		if pattern_lib.has_key(pattern):
			value = pattern_lib[pattern]+1
			pattern_lib[pattern]=value
		else:
			pattern_lib[pattern]=1
		pastr = pattern.replace('L',' ').replace('U',' ').replace('D',' ').replace('S',' ')
		sbox = [];
		for i in pattern:
			if i in "LUDS":
				sbox.append(i)
		offset = 0
		n = 0
		# update markov 
		ptable = pastr.split()
		for i in ptable:	# deal with each substring
			length = int(i)
			if sbox[n] == "L":
				sub = psswd[offset:offset+length]	# get that substring
				if lower_occurence.has_key(length):
					if lower_occurence[length].has_key(sub):
						lower_occurence[length][sub] += 1
					else:
						lower_occurence[length][sub] = 1
				else:
					lower_occurence[length] = {sub:1}
				lower_firsthit[psswd[offset]] = lower_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					lower_markov[psswd[j]][lowercase.find(psswd[j+1])] += 1
					j = j+1
			elif sbox[n] == "U":
				sub = psswd[offset:offset+length]	# get that substring
				if upper_occurence.has_key(length):
					if upper_occurence[length].has_key(sub):
						upper_occurence[length][sub] += 1
					else:
						upper_occurence[length][sub] = 1
				else:
					upper_occurence[length] = {sub:1}
				upper_firsthit[psswd[offset]] = upper_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					upper_markov[psswd[j]][uppercase.find(psswd[j+1])] += 1
					j = j+1
			elif sbox[n] == "D":	
				sub = psswd[offset:offset+length]	# get that substring
				if digit_occurence.has_key(length):
					if digit_occurence[length].has_key(sub):
						digit_occurence[length][sub] += 1
					else:
						digit_occurence[length][sub] = 1
				else:
					digit_occurence[length] = {sub:1}
				digit_firsthit[psswd[offset]] = digit_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					digit_markov[psswd[j]][digit.find(psswd[j+1])] += 1
					j = j+1
			else:
				sub = psswd[offset:offset+length]	# get that substring
				if symbol_occurence.has_key(length):
					if symbol_occurence[length].has_key(sub):
						symbol_occurence[length][sub] += 1
					else:
						symbol_occurence[length][sub] = 1
				else:
					symbol_occurence[length] = {sub:1}
				symbol_firsthit[psswd[offset]] = symbol_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					symbol_markov[psswd[j]][symbol.find(psswd[j+1])] += 1
					j = j+1
			offset = offset + length
			n = n + 1
	#print lower_markov.viewitems(), upper_markov.viewitems(), digit_markov.viewitems(), symbol_markov.viewitems()
	print lower_occurence[4].viewitems()




if __name__ == "__main__":
	assert len(sys.argv) == 2, "correct usage: make_markov.py <passwords_file>"
	main(sys.argv[1])
