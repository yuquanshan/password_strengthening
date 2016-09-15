# Introduction 
The password strength is reflected by guess probability which is based on Markov chain and PCFG (Probabilistic Context-Free Grammars).

# How to use

## PCFGModel.py

It's used for PCFG-Markov(1-gram) based password strength estimation, see Eq. (1) and (2) in the [paper](http://www.cse.psu.edu/~trj1/papers/acsac13.pdf). It contains a class (PCFGModel) which contains the following attributes and methods:

	characters	-	all possible characters which could appear in the password
	lowercase 	- 	all possible lowrecase characters which could appear in the password
	uppercase 	- 	all possible uppercase characters which could appear in the password
	digit		-	all possible digits which could appear in the password
	symbol 		- 	all possible symbols which could appear in the password, note that it will grow in the training phase (there could be extra UTF-8 symbols to deal with)
	
	pattern_lib	- 	a {pattern:occurence} dictionary storing all patterns and their occurences in the training set
	
	lower_occurence	-	a {length:{sub:occurence}} dictionary storing the occurences of lowercase substrings
	upper_occurence	- 	a {length:{sub:occurence}} dictionary storing the occurences of uppercase substrings
	digit_occurence	- 	a {length:{sub:occurence}} dictionary storing the occurences of digit substrings
	symbol_occurence-	a {length:{sub:occurence}} dictionary storing the occurences of symbol substrings

	lower_occurence_sum	-	a {length:sum}	dictionary storing the total occurence of lowercase substrings with a certain length (in order to accelerate computing)
	upper_occurence_sum	-	a {length:sum} dictionary storing the total occurence of uppercase substrings with a certain length
	digit_occurence_sum	-	a {length:sum} dictionary storing the total occurence of digit substrings with a certain length
	symbol_occurence_sum-	a {length:sum} dictionary storing the total occurence of symbol substrings with a certain length 
	
	lower_firsthit	- 	a {char:occurence} dictionary storing the occurences of the case where a lowercase character appears first in its substring
	upper_firsthit  -       a {char:occurence} dictionary storing the occurences of the case where a uppercase character appears first in its substring
	digit_firsthit  -       a {char:occurence} dictionary storing the occurences of the case where a digit character appears first in its substring
	symbol_firsthit -       a {char:occurence} dictionary storing the occurences of the case where a symbol character appears first in its substring, note that it may grow in the training phase
	
	lower_markov 	-	a {char:list} dictionary storing the markov chain(table) of all lowercase substring
	upper_markov    -       a {char:list} dictionary storing the markov chain(table) of all uppercase substring
	digit_markov    -       a {char:list} dictionary storing the markov chain(table) of all digit substring
	symbol_markov   -       a {char:list} dictionary storing the markov chain(table) of all symbol substring
	
	getPattern(string)	- 	return a pattern of a string, e.g., if the input is "hello123", it turns "L5D3"
	train(file)		- 	train the model with the input file, e.g., train("[rockyou.txt](http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2)")
	getGP(string)		-	calculate the guess probability of a password string (you need to train the model first) 	

A more concrete example:

	from PCFGModel import PCFGModel
	model = PCFGModel()
	model.train("rockyou.txt")	# will take about 4 min to train
	model.getGP("hello123")		# will return the GP of password "hello123"
	
Alternative you can skip over the training set, since there is a serialized model (trained on "rockyou.txt") available at my [site](http://www.cse.psu.edu/~yxs182/jumpstart.pkl). After downloading it, you can deserialze it by:
	
	from PCFGModel import PCFGModel
	model = PCFGModel()
	model.deserializeModel('jumpstart.pkl')	# will take about half minute, which is much shorter
	
There are jumpstart scripts available, the first version is single process version:
	
	python jumpstart.py rockyou.txt.6.4 	# strengthen rockyou.txt.6.4 based on jumpstart.pkl
	
the second version is faster multiprocess version (split the to-be-strengthened file into multiple parts and create multiple parallel process to strengthen their own part, unfortunately they can't share updated model yet):

	python jumpstart_multiprocess.py rockyou.txt.6.4 3	# create three processes to strengthen rockyou.txt.6.4
	
