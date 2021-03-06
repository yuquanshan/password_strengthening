#!/usr/bin/python

# gram-1 markov stats for each of the patterns
# 	L: lowercase letter
#	U: uppercase letter
# 	D: digit
# 	S: symbol


import sys,os,copy,math,random,pickle,threading,time
class PCFGModel:
# all possible password characters
	def __init__(self):
		self.characters = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
		self.lowercase = "abcdefghijklmnopqrstuvwxyz"
		self.uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.digit = "0123456789"
		self.symbol = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
		self.symbolLen = len(self.symbol)-1
		random.seed(time.time)
		#self.lock = threading.lock()	# in order to protect model data in multithread

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
		self.lower_occurence_sum = {}	#{length:occurence_sum}
		self.upper_occurence_sum = {}
		self.digit_occurence_sum = {}
		self.symbol_occurence_sum = {}
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
			if len(l.replace('\n','')) != 0:
				psswd = l.replace('\n','')
				self.updateNew(psswd)

	def updateNew(self, psswd):	# update pattern library, markov structure
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
					self.lower_occurence_sum[length] += 1
					if self.lower_occurence[length].has_key(sub):
						self.lower_occurence[length][sub] += 1
					else:
						self.lower_occurence[length][sub] = 1
				else:
					self.lower_occurence[length] = {sub:1}
					self.lower_occurence_sum[length] = 1
				self.lower_firsthit[psswd[offset]] = self.lower_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					self.lower_markov[psswd[j]][self.lowercase.find(psswd[j+1])] += 1
					j = j+1
			elif sbox[n] == "U":
				sub = psswd[offset:offset+length]	# get that substring
				if self.upper_occurence.has_key(length):
					self.upper_occurence_sum[length] += 1
					if self.upper_occurence[length].has_key(sub):
						self.upper_occurence[length][sub] += 1
					else:
						self.upper_occurence[length][sub] = 1
				else:
					self.upper_occurence[length] = {sub:1}
					self.upper_occurence_sum[length] = 1
				self.upper_firsthit[psswd[offset]] = self.upper_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					self.upper_markov[psswd[j]][self.uppercase.find(psswd[j+1])] += 1
					j = j+1
			elif sbox[n] == "D":	
				sub = psswd[offset:offset+length]	# get that substring
				if self.digit_occurence.has_key(length):
					self.digit_occurence_sum[length] += 1
					if self.digit_occurence[length].has_key(sub):
						self.digit_occurence[length][sub] += 1
					else:
						self.digit_occurence[length][sub] = 1
				else:
					self.digit_occurence[length] = {sub:1}
					self.digit_occurence_sum[length] = 1
				self.digit_firsthit[psswd[offset]] = self.digit_firsthit[psswd[offset]]+1
				j = offset
				while(j<offset+length-1):
					self.digit_markov[psswd[j]][self.digit.find(psswd[j+1])] += 1
					j = j+1
			else:
				sub = psswd[offset:offset+length]	# get that substring
				if self.symbol_occurence.has_key(length):
					self.symbol_occurence_sum[length] += 1
					if self.symbol_occurence[length].has_key(sub):
						self.symbol_occurence[length][sub] += 1
					else:
						self.symbol_occurence[length][sub] = 1
				else:
					self.symbol_occurence[length] = {sub:1}
					self.symbol_occurence_sum[length] = 1
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
			return 1
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
				if gp == 0:
					return 0
				length = int(i);	
				sub = psswd[offset:offset+length]
				ob_freq = float(0)		# observed frequence in (1) of pitfall paper
				chain_prob = float(0)	# prob derived from markov chain in (1) of pitfall paper
				if sbox[n] == 'L':
					if self.lower_occurence.has_key(length):
						if self.lower_occurence[length].has_key(sub):
							ob_freq = float(self.lower_occurence[length][sub])/self.lower_occurence_sum[length]
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.lower_firsthit.has_key(sub[0]):
						chain_prob = float(self.lower_firsthit[sub[0]])/sum(self.lower_firsthit.values())
						for j in range(0,length-1): 	# then calculate transition part of the prob
							if sum(self.lower_markov[sub[j]]) == 0:
								chain_prob = 0
							else:
								chain_prob = chain_prob*float(self.lower_markov[sub[j]][self.lowercase.find(sub[j+1])])/sum(self.lower_markov[sub[j]])
					else:
						chain_prob = 0
					#print ob_freq, chain_prob
					gp = gp*max(ob_freq,chain_prob)
				elif sbox[n] == 'U':
					if self.upper_occurence.has_key(length):
						if self.upper_occurence[length].has_key(sub):
							ob_freq = float(self.upper_occurence[length][sub])/self.upper_occurence_sum[length]
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.upper_firsthit.has_key(sub[0]):
						chain_prob = float(self.upper_firsthit[sub[0]])/sum(self.upper_firsthit.values())
						for j in range(0,length-1):
							if sum(self.upper_markov[sub[j]]) == 0:
								chain_prob = 0
							else:
								chain_prob = chain_prob*float(self.upper_markov[sub[j]][self.uppercase.find(sub[j+1])])/sum(self.upper_markov[sub[j]])
					else:
						chain_prob = 0
					gp = gp*max(ob_freq,chain_prob)
				elif sbox[n] == 'D':
					if self.digit_occurence.has_key(length):
						if self.digit_occurence[length].has_key(sub):
							ob_freq = float(self.digit_occurence[length][sub])/self.digit_occurence_sum[length]
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.digit_firsthit.has_key(sub[0]):
						chain_prob = float(self.digit_firsthit[sub[0]])/sum(self.digit_firsthit.values())
						for j in range(0,length-1):
							if sum(self.digit_markov[sub[j]]) == 0:
								chain_prob = 0;
							else:
								chain_prob = chain_prob*float(self.digit_markov[sub[j]][self.digit.find(sub[j+1])])/sum(self.digit_markov[sub[j]])
					else:
						chain_prob = 0
					gp = gp*max(ob_freq,chain_prob)
				else:
					if self.symbol_occurence.has_key(length):
						if self.symbol_occurence[length].has_key(sub):
							ob_freq = float(self.symbol_occurence[length][sub])/self.symbol_occurence_sum[length]
						else:
							ob_freq = 0
					else:
						ob_freq = 0
					if self.symbol_firsthit.has_key(sub[0]):
						chain_prob = float(self.symbol_firsthit[sub[0]])/sum(self.symbol_firsthit.values())
						for j in range(0,length-1):
							if sum(self.symbol_markov[sub[j]]) == 0:
								chain_prob = 0;
							else:
								chain_prob = chain_prob*float(self.symbol_markov[sub[j]][self.symbol.find(sub[j+1])])/sum(self.symbol_markov[sub[j]])
					else:
						chain_prob = 0
					gp = gp*max(ob_freq,chain_prob)
				offset = offset + length
				n = n+1
			return gp
		else:	# this pattern is currently not in the pattern library
			return 0

	def clearOld(self, psswd):	# clear the old password from the PCFG model records, symmetric to updateNew
		pattern = self.getPattern(psswd)
		if self.pattern_lib.has_key(pattern):
			value = self.pattern_lib[pattern]-1
			self.pattern_lib[pattern]=value
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
					self.lower_occurence_sum[length] -= 1
					if self.lower_occurence[length].has_key(sub):
						self.lower_occurence[length][sub] -= 1
				self.lower_firsthit[psswd[offset]] = self.lower_firsthit[psswd[offset]]-1
				j = offset
				while(j<offset+length-1):
					self.lower_markov[psswd[j]][self.lowercase.find(psswd[j+1])] -= 1
					j = j+1
			elif sbox[n] == "U":
				sub = psswd[offset:offset+length]	# get that substring
				if self.upper_occurence.has_key(length):
					self.upper_occurence_sum[length] -= 1
					if self.upper_occurence[length].has_key(sub):
						self.upper_occurence[length][sub] -= 1
				self.upper_firsthit[psswd[offset]] = self.upper_firsthit[psswd[offset]]-1
				j = offset
				while(j<offset+length-1):
					self.upper_markov[psswd[j]][self.uppercase.find(psswd[j+1])] -= 1
					j = j+1
			elif sbox[n] == "D":	
				sub = psswd[offset:offset+length]	# get that substring
				if self.digit_occurence.has_key(length):
					self.digit_occurence_sum[length] -= 1
					if self.digit_occurence[length].has_key(sub):
						self.digit_occurence[length][sub] -= 1
				self.digit_firsthit[psswd[offset]] = self.digit_firsthit[psswd[offset]]-1
				j = offset
				while(j<offset+length-1):
					self.digit_markov[psswd[j]][self.digit.find(psswd[j+1])] -= 1
					j = j+1
			else:
				sub = psswd[offset:offset+length]	# get that substring
				if self.symbol_occurence.has_key(length):
					self.symbol_occurence_sum[length] -= 1
					if self.symbol_occurence[length].has_key(sub):
						self.symbol_occurence[length][sub] -= 1
				if self.symbol_firsthit.has_key(psswd[offset]):
					self.symbol_firsthit[psswd[offset]] = self.symbol_firsthit[psswd[offset]]-1	
				j = offset
				while(j<offset+length-1):
					self.symbol_markov[psswd[j]][self.symbol.find(psswd[j+1])] -= 1							
					j = j+1
			offset = offset + length
			n = n + 1

	def update(self, oldpsswd, newpsswd):	# delete the old password entry and update new password
		self.updateNew(newpsswd)
		self.clearOld(oldpsswd)

	#print lower_markov.viewitems(), upper_markov.viewitems(), digit_markov.viewitems(), symbol_markov.viewitems()
	#print lower_occurence[4].viewitems()

	def allThreePos(self,len):	# using DFS to find all possible three positions to change, of course, len must >= 3
		pool = range(0,len)
		res = []
		for i in range(0,len-2):
			tmp = self.visit([i],pool,2)
			res = res+tmp
		return res

	def visit(self, psselems, pool, left):
		res = []
		pos = pool.index(psselems[-1])+1
		if(left == 1):
			j = pos
			while(j<len(pool)):
				tmp = copy.copy(psselems)
				tmp.append(pool[j])
				res.append(tmp)
				j+=1
		else:
			j = pos
			while(j<len(pool)-left+1):
				tmp = copy.copy(psselems)
				tmp.append(pool[j])
				res = res+self.visit(tmp,pool,left-1)
				j+=1
		return res

	def typeOfChar(self,char):
		if char in self.lowercase:
			return 'L'
		elif char in self.uppercase:
			return 'U'
		elif char in self.digit:
			return 'D'
		else:
			return 'S'

	def strengthen(self,psswd):	# strengthen the psswd, return the strengthened result, if the password's GP is smaller than 10^-20, then it's good to go
		length = len(psswd)
		maxTry = 5				# max number of position number tries
		buff = 10
		last = 0
		if(length == 1):
			res = self.rareFirstHit('LUDS')
			return res
		elif(length == 2):
			candi = psswd
			lowestGPSoFar = self.getGP(psswd) 
			for i in 'LUDS':
				for j in 'LUDS':
					tmp = self.rareFirstHit(i)
					if i == j:
						if i == 'L':
							tmp = tmp + self.lowercase[self.randomPickMarkov(self.lower_markov[tmp],'L',10)]
						elif i == 'U':
							tmp = tmp + self.uppercase[self.randomPickMarkov(self.upper_markov[tmp],'U',10)]
						elif i == 'D':
							tmp = tmp + self.digit[self.randomPickMarkov(self.digit_markov[tmp],'D',5)]
						else:
							tmp = tmp + self.symbol[self.randomPickMarkov(self.symbol_markov[tmp],'S',10)]
					else:
						tmp = tmp+self.rareFirstHit(j)
					tmpGP = self.getGP(tmp)
					if tmpGP < lowestGPSoFar:
						candi = tmp
						lowestGPSoFar = tmpGP
			return candi
		elif(length <= 5):
			pos = self.allThreePos(length)
			#posSize = len(pos)
			pattern = self.getPattern(psswd)
			#starts = self.startPos(pattern)
			candi = psswd
			lowestGPSoFar = self.getGP(psswd)
			for p in pos:
				if lowestGPSoFar < math.pow(10,-16):
					break
				tmpPass = psswd
				tmpPatt = pattern
				#tmpStar = starts
				for i in p:
					if(i == 0):
						tmpPass = tmpPass[:i] + self.rareFirstHit('LUDS') + tmpPass[i+1:]
						tmpPatt = self.getPattern(tmpPass)
						#tmpStar = self.startPos(tmpPatt)
					else:
						tb = self.typeOfChar(tmpPass[i-1])
						tmpPass1 = tmpPass[:i] + self.rareFirstHit('LUDS'.replace(tb,'')) + tmpPass[i+1:]
						if tb == 'L':
							tmpPass2 = tmpPass[:i] + self.lowercase[self.randomPickMarkov(self.lower_markov[tmpPass[i-1]],'L',10)] + tmpPass[i+1:]
						elif tb == 'U':
							tmpPass2 = tmpPass[:i] + self.uppercase[self.randomPickMarkov(self.upper_markov[tmpPass[i-1]],'U',10)] + tmpPass[i+1:]
						elif tb == 'D':
							tmpPass2 = tmpPass[:i] + self.digit[self.randomPickMarkov(self.digit_markov[tmpPass[i-1]],'D',5)] + tmpPass[i+1:]
						else:
							tmpPass2 = tmpPass[:i] + self.symbol[self.randomPickMarkov(self.symbol_markov[tmpPass[i-1]],'S',10)] + tmpPass[i+1:]
						if self.getGP(tmpPass1) < self.getGP(tmpPass2):
							tmpPass = tmpPass1
						else:
							tmpPass = tmpPass2
						tmpPatt = self.getPattern(tmpPass)
						#tmpStar = self.startPos(tmpPatt)
				tmpGP = self.getGP(tmpPass)
				if(tmpGP < lowestGPSoFar):
					lowestGPSoFar = tmpGP
					candi = tmpPass
			return candi
		elif(length <= 25):
			pos = self.allThreePos(length)
			posSize = len(pos)
			pattern = self.getPattern(psswd)
			#starts = self.startPos(pattern)
			candi = psswd
			lowestGPSoFar = self.getGP(psswd)
			tried = set([])	# record already-tried position sets
			count = 1 	# try count
			while(count <= maxTry):
				if lowestGPSoFar < math.pow(10,-18):
					break
				indp = random.randint(0,posSize-1)
				while(indp in tried):	# until new position set appears
					indp = random.randint(0,posSize-1)
				tried.add(indp)
				p = pos[indp]

				tmpPass = psswd
				tmpPatt = pattern
				for i in p:	
					if(i == 0):
						tmpPass = tmpPass[:i] + self.rareFirstHit('LUDS') + tmpPass[i+1:]
						tmpPatt = self.getPattern(tmpPass)
						#tmpStar = self.startPos(tmpPatt)
					else:
						tb = self.typeOfChar(tmpPass[i-1])
						tmpPass1 = tmpPass[:i] + self.rareFirstHit('LUDS'.replace(tb,'')) + tmpPass[i+1:]
						if tb == 'L':
							tmpPass2 = tmpPass[:i] + self.lowercase[self.randomPickMarkov(self.lower_markov[tmpPass[i-1]],'L',10)] + tmpPass[i+1:]
						elif tb == 'U':
							tmpPass2 = tmpPass[:i] + self.uppercase[self.randomPickMarkov(self.upper_markov[tmpPass[i-1]],'U',10)] + tmpPass[i+1:]
						elif tb == 'D':
							tmpPass2 = tmpPass[:i] + self.digit[self.randomPickMarkov(self.digit_markov[tmpPass[i-1]],'D',5)] + tmpPass[i+1:]
						else:
							tmpPass2 = tmpPass[:i] + self.symbol[self.randomPickMarkov(self.symbol_markov[tmpPass[i-1]],'S',10)] + tmpPass[i+1:]
						if self.getGP(tmpPass1) < self.getGP(tmpPass2):
							tmpPass = tmpPass1
						else:
							tmpPass = tmpPass2
						tmpPatt = self.getPattern(tmpPass)
						#tmpStar = self.startPos(tmpPatt)
				tmpGP = self.getGP(tmpPass)
				if(tmpGP < lowestGPSoFar):
					lowestGPSoFar = tmpGP
					candi = tmpPass
				count+=1
			return candi
		else:
			candi = psswd
			for i in range(0,3):
				if self.getGP(candi) < math.pow(10,-18):
					break
				j = random.randint(0,length-1)
				candi = candi[:j] + self.rareFirstHit('LUDS') + candi[j+1:]
			return candi

	def startPos(pattern):	# given a pattern, return all starting position of each substring
		pastr = pattern.replace('L',' ').replace('U',' ').replace('D',' ').replace('S',' ').split()
		offset = 0
		res = [offset]
		for i in range(0,len(pastr)-1):
			offset = offset + int(pastr[i])
			res.append(offset)
		return res

	
	def rareFirstHit(self,cat):
		buff = 10
		last = 0
		box = []
		tar = []
		if 'L' in cat:
			for i in self.lowercase:
				if len(box) <= buff:
					box.append(self.lower_firsthit[i])
					tar.append(i)
					if self.lower_firsthit[i] > last:
						last = self.lower_firsthit[i]
				else:
					if self.lower_firsthit[i] < last:
						ind = box.index(last)
						box.pop(ind)
						tar.pop(ind)
						box.append(self.lower_firsthit[i])
						tar.append(i)
						last = sorted(box)[-1]
		if 'U' in cat:
			for i in self.uppercase:
				if len(box) <= buff:
					box.append(self.upper_firsthit[i])
					tar.append(i)
					if self.upper_firsthit[i] > last:
						last= self.upper_firsthit[i]
				else:
					if self.upper_firsthit[i] < last:
						ind = box.index(last)
						box.pop(ind)
						tar.pop(ind)
						box.append(self.upper_firsthit[i])
						tar.append(i)
						last = sorted(box)[-1]
		if 'D' in cat:
			for i in self.digit:
				if len(box) <= buff:
					box.append(self.digit_firsthit[i])
					tar.append(i)
					if self.digit_firsthit[i] > last:
						last = self.digit_firsthit[i]
				else:
					if self.digit_firsthit[i] < last:
						ind = box.index(last)
						box.pop(ind)
						tar.pop(ind)
						box.append(self.digit_firsthit[i])
						tar.append(i)
						last = sorted(box)[-1]
		if 'S' in cat:
			for i in self.symbol[:self.symbolLen]:
				if len(box) <= buff:
					box.append(self.symbol_firsthit[i])
					tar.append(i)
					if self.symbol_firsthit[i] > last:
						last = self.symbol_firsthit[i]
				else:
					if self.symbol_firsthit[i] < last:
						ind = box.index(last)
						box.pop(ind)
						tar.pop(ind)
						box.append(self.symbol_firsthit[i])
						tar.append(i)
						last = sorted(box)[-1]
		return tar[random.randint(0,9)]	# randomly choose one from 10 candidates

	def strengthenFile(self, filename):	# single thread only
		fi = file(filename,'r')
		lines = fi.readlines()
		fi.close()
		#newpool = ''
		fi = file(filename+'.strengthened','w')
		count = 0
		for l in lines:
			if len(l.replace('\n','')) != 0:
				psswd = l.replace('\n','')
				newpsswd = self.strengthen(psswd)
				self.update(psswd,newpsswd)
				count += 1
				if count%100 == 0:
					print "PROGRESS: " + str(count) + " passwords strengthened."
				#newpool = newpool+newpsswd+'\n'
				fi.write(newpsswd+'\n')
		#fi.write(newpool)
		fi.close()

	def randomPickMarkov(self,chain,which,num):	# e.g., self.randomPickMarkov(symbol_markov['?'],'S',10) - randomly choose 10 symbols in chain symbol_markov['?'], pick the smallest one
		poolLen = 0
		if which == 'L':
			poolLen = len(self.lowercase)
		elif which == 'U':
			poolLen = len(self.uppercase)
		elif which in 'D':
			poolLen = len(self.digit)
		else:
			poolLen = self.symbolLen
		pool = range(0,poolLen)
		count = 1
		lowest = 100000000
		ind = 0
		while(count <= num):
			rid = random.randint(0,poolLen-1)
			tmpi = pool[rid]
			if chain[tmpi] < lowest:
				ind = tmpi
				lowest = chain[tmpi]
			pool.pop(rid)
			poolLen -= 1
			count+=1
		return ind

	def test_getAllGP(self,filename):
		fi = file(filename,'r')
		lines = fi.readlines()
		fi.close()
		count = 1
		for l in lines:
			s = l.replace('\n','')
			self.getGP(s)
			if count%100 == 0:
				print "PROCESS: "+str(count)+" GPs calculated."
			count+=1

	def serializeModel(self,filename):
		fo = file(filename,'wb')
		pickle.dump(self.characters,fo,-1)
		pickle.dump(self.lowercase,fo,-1)
		pickle.dump(self.uppercase,fo,-1)
		pickle.dump(self.digit,fo,-1)
		pickle.dump(self.symbol,fo,-1)

		pickle.dump(self.pattern_lib,fo,-1)

		pickle.dump(self.lower_occurence,fo,-1)
		pickle.dump(self.upper_occurence,fo,-1)
		pickle.dump(self.digit_occurence,fo,-1)
		pickle.dump(self.symbol_occurence,fo,-1)

		pickle.dump(self.lower_occurence_sum,fo,-1)
		pickle.dump(self.upper_occurence_sum,fo,-1)
		pickle.dump(self.digit_occurence_sum,fo,-1)
		pickle.dump(self.symbol_occurence_sum,fo,-1)

		pickle.dump(self.lower_firsthit,fo,-1)
		pickle.dump(self.upper_firsthit,fo,-1)
		pickle.dump(self.digit_firsthit,fo,-1)
		pickle.dump(self.symbol_firsthit,fo,-1)

		pickle.dump(self.lower_markov,fo,-1)
		pickle.dump(self.upper_markov,fo,-1)
		pickle.dump(self.digit_markov,fo,-1)
		pickle.dump(self.symbol_markov,fo,-1)

		pickle.dump(self.symbolLen,fo,-1)
		fo.close()

	def deserializeModel(self,filename):
		fi = file(filename,'rb')
	
		self.characters = pickle.load(fi)
		
		self.lowercase = pickle.load(fi)
		self.uppercase = pickle.load(fi)
		self.digit = pickle.load(fi)
		self.symbol = pickle.load(fi)

		self.pattern_lib = pickle.load(fi)

		self.lower_occurence = pickle.load(fi)
		self.upper_occurence = pickle.load(fi)
		self.digit_occurence = pickle.load(fi)
		self.symbol_occurence = pickle.load(fi)

		self.lower_occurence_sum = pickle.load(fi)
		self.upper_occurence_sum = pickle.load(fi)
		self.digit_occurence_sum = pickle.load(fi)
		self.symbol_occurence_sum = pickle.load(fi)

		self.lower_firsthit = pickle.load(fi)
		self.upper_firsthit = pickle.load(fi)
		self.digit_firsthit = pickle.load(fi)
		self.symbol_firsthit = pickle.load(fi)

		self.lower_markov = pickle.load(fi)
		self.upper_markov = pickle.load(fi)
		self.digit_markov = pickle.load(fi)
		self.symbol_markov = pickle.load(fi)

		self.symbolLen = pickle.load(fi)
		fi.close()

#if __name__ == "__main__":
#	assert len(sys.argv) == 2, "correct usage: make_markov.py <passwords_file>"
#	main(sys.argv[1])
