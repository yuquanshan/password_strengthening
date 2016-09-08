#!/usr/bin/python

# gram-1 markov stats for each of the patterns
# 	L: lowercase letter
#	U: uppercase letter
# 	D: digit
# 	S: symbol


import sys,os
class PCFGModel:
# all possible password characters
	def __init__(self):
		self.characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
		self.lowercase = "abcdefghijklmnopqrstuvwxyz"
		self.uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.digit = "0123456789"
		self.symbol = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

	def getPattern(self,psswd):
		length = len(psswd)
		pattern = ""
		head = ""
		counter = 0
		for i in range(0,length):
			if psswd[i] in self.lowercase:
				if head == "L":
					counter = counter+1
				else:
					if head != "":
						pattern = pattern+head+str(counter)
					head = "L"
					counter = 1
			elif psswd[i] in self.uppercase:
				if head == "U":
					counter = counter+1
				else:
					if head != "":
						pattern = pattern+head+str(counter)
					head = "U"
					counter = 1 
			elif psswd[i] in self.digit:
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

	def train(self,filename):
		fi = file(filename,'r')
		lines = fi.readlines()
		fi.close()
		#output = file(filename+'.gram1mc','w')
		#output.write("possible characters: "+characters+'\n')
		# study the pattern of each password in the password database
		self.pattern_lib = {}	# record patterns occurence
		self.lower_occurence = {}	#{length:{psswd:occurence}}
		self.upper_occurence = {}	
		self.digit_occurence = {}
		self.symbol_occurence = {}
		self.lower_markov = {}
		self.lower_firsthit = {}
		for i in self.lowercase:
			self.lower_markov[i] = [0]*len(self.lowercase)
			self.lower_firsthit[i] = 0
		self.upper_markov = {}
		self.upper_firsthit = {}
		for i in self.uppercase:
			self.upper_markov[i] = [0]*len(self.uppercase)
			self.upper_firsthit[i] = 0
		self.digit_markov = {}
		self.digit_firsthit = {}
		for i in self.digit:
			self.digit_markov[i] = [0]*len(self.digit)
			self.digit_firsthit[i] = 0
		self.symbol_markov = {}
		self.symbol_firsthit = {}
		for i in self.symbol:
			self.symbol_markov[i] = [0]*len(self.symbol)
			self.symbol_firsthit[i] = 0
		for l in lines:
			if len(l.split()) != 0:
				psswd = l.split()[0];
				pattern = self.getPattern(psswd)
				if self.pattern_lib.has_key(pattern):
					value = self.pattern_lib[pattern]+1
					self.pattern_lib[pattern]=value
				else:
					self.pattern_lib[pattern]=1
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
						if self.lower_occurence.has_key(length):
							if self.lower_occurence[length].has_key(sub):
								self.lower_occurence[length][sub] += 1
							else:
								self.lower_occurence[length][sub] = 1
						else:
							self.lower_occurence[length] = {sub:1}
						self.lower_firsthit[psswd[offset]] = self.lower_firsthit[psswd[offset]]+1
						j = offset
						while(j<offset+length-1):
							self.lower_markov[psswd[j]][self.lowercase.find(psswd[j+1])] += 1
							j = j+1
					elif sbox[n] == "U":
						sub = psswd[offset:offset+length]	# get that substring
						if self.upper_occurence.has_key(length):
							if self.upper_occurence[length].has_key(sub):
								self.upper_occurence[length][sub] += 1
							else:
								self.upper_occurence[length][sub] = 1
						else:
							self.upper_occurence[length] = {sub:1}
						self.upper_firsthit[psswd[offset]] = self.upper_firsthit[psswd[offset]]+1
						j = offset
						while(j<offset+length-1):
							self.upper_markov[psswd[j]][self.uppercase.find(psswd[j+1])] += 1
							j = j+1
					elif sbox[n] == "D":	
						sub = psswd[offset:offset+length]	# get that substring
						if self.digit_occurence.has_key(length):
							if self.digit_occurence[length].has_key(sub):
								self.digit_occurence[length][sub] += 1
							else:
								self.digit_occurence[length][sub] = 1
						else:
							self.digit_occurence[length] = {sub:1}
						self.digit_firsthit[psswd[offset]] = self.digit_firsthit[psswd[offset]]+1
						j = offset
						while(j<offset+length-1):
							self.digit_markov[psswd[j]][self.digit.find(psswd[j+1])] += 1
							j = j+1
					else:
						sub = psswd[offset:offset+length]	# get that substring
						if self.symbol_occurence.has_key(length):
							if self.symbol_occurence[length].has_key(sub):
								self.symbol_occurence[length][sub] += 1
							else:
								self.symbol_occurence[length][sub] = 1
						else:
							self.symbol_occurence[length] = {sub:1}
						if self.symbol_firsthit.has_key(psswd[offset]):
							self.symbol_firsthit[psswd[offset]] = self.symbol_firsthit[psswd[offset]]+1
						else:
							self.symbol_firsthit[psswd[offset]] = 1
							self.symbol = self.symbol+psswd[offset]
							self.characters = self.characters+psswd[offset]
							for k in self.symbol_markov.keys():
								self.symbol_markov[k].append(0)
							self.symbol_markov[psswd[offset]] = [0]*len(self.symbol)	
						j = offset
						while(j<offset+length-1):
							if not self.symbol_firsthit.has_key(psswd[j+1]):
								self.symbol_firsthit[psswd[j+1]] = 0
								self.symbol = self.symbol+psswd[j+1]
								self.characters = self.characters+psswd[j+1]
								for k in self.symbol_markov.keys():
									self.symbol_markov[k].append(0)
								self.symbol_markov[psswd[j+1]] = [0]*len(self.symbol)
							self.symbol_markov[psswd[j]][self.symbol.find(psswd[j+1])] += 1							
							j = j+1
					offset = offset + length
					n = n + 1
	def getGP(self, psswd):	# calculate the guess probability of a password (psswd)
		if len(psswd) == 0:	# meaning psswd is empty, then 100% cracking probability apparently
			return 1;
		pattern = self.getPattern(psswd);
		if(self.pattern_lib.has_key(pattern)):
			gp = float(self.pattern_lib[pattern])/sum(self.pattern_lib.values())
			pastr = pattern.replace('L',' ').replace('U',' ').replace('D',' ').replace('S',' ')
			sbox = [];
			for i in pattern:
				if i in "LUDS":
					sbox.append(i)
			offset = 0
			n = 0 
			ptable = pastr.split()
			for i in ptable:	# calculate GP for each substring
				length = int(i);	
				sub = psswd[offset:offset+length]
				ob_freq = float(0)		# observed frequence in (1) of pitfall paper
				chain_prob = float(0)	# prob derived from markov chain in (1) of pitfall paper
				if sbox[n] == 'L':
					if self.lower_occurence.has_key(length):
						if self.lower_occurence[length].has_key(sub):
							ob_freq = float(self.lower_occurence[length][sub])/sum(self.lower_occurence[length].values())
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.lower_firsthit.has_key(sub[0]):
						chain_prob = float(self.lower_firsthit[sub[0]])/sum(self.lower_firsthit.values())
						for j in range(0,length-1): 	# then calculate transition part of the prob
							chain_prob = chain_prob*float(self.lower_markov[sub[j]][self.lowercase.find(sub[j+1])])/sum(self.lower_markov[sub[j]])
					else:
						chain_prob = 0
					#print ob_freq, chain_prob
					gp = gp*max(ob_freq,chain_prob)
				elif sbox[n] == 'U':
					if self.upper_occurence.has_key(length):
						if self.upper_occurence[length].has_key(sub):
							ob_freq = float(self.upper_occurence[length][sub])/sum(self.upper_occurence[length].values())
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.upper_firsthit.has_key(sub[0]):
						chain_prob = float(self.upper_firsthit[sub[0]])/sum(self.upper_firsthit.values())
						for j in range(0,length-1):
							chain_prob = chain_prob*float(self.upper_markov[sub[j]][self.uppercase.find(sub[j+1])])/sum(self.upper_markov[sub[j]])
					else:
						chain_prob = 0
					gp = gp*max(ob_freq,chain_prob)
				elif sbox[n] == 'D':
					if self.digit_occurence.has_key(length):
						if self.digit_occurence[length].has_key(sub):
							ob_freq = float(self.digit_occurence[length][sub])/sum(self.digit_occurence[length].values())
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.digit_firsthit.has_key(sub[0]):
						chain_prob = float(self.digit_firsthit[sub[0]])/sum(self.digit_firsthit.values())
						for j in range(0,length-1):
							chain_prob = chain_prob*float(self.digit_markov[sub[j]][self.digit.find(sub[j+1])])/sum(self.digit_markov[sub[j]])
					else:
						chain_prob = 0
					gp = gp*max(ob_freq,chain_prob)
				else:
					if self.symbol_occurence.has_key(length):
						if self.symbol_occurence[length].has_key(sub):
							ob_freq = float(self.symbol_occurence[length][sub])/sum(self.symbol_occurence[length].values())
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.symbol_firsthit.has_key(sub[0]):
						chain_prob = float(self.symbol_firsthit[sub[0]])/sum(self.symbol_firsthit.values())
						for j in range(0,length-1):
							chain_prob = chain_prob*float(self.symbol_markov[sub[j]][self.symbol.find(sub[j+1])])/sum(self.symbol_markov[sub[j]])
					else:
						chain_prob = 0
					gp = gp*max(ob_freq,chain_prob)
				offset = offset + length
				n = n+1
			return gp
		else:	# this pattern is currently not in the pattern library
			return 0;


	#print lower_markov.viewitems(), upper_markov.viewitems(), digit_markov.viewitems(), symbol_markov.viewitems()
	#print lower_occurence[4].viewitems()




#if __name__ == "__main__":
#	assert len(sys.argv) == 2, "correct usage: make_markov.py <passwords_file>"
#	main(sys.argv[1])
