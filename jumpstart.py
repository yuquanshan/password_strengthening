#!/usr/bin/python

# a jumpstart script to strengthen a file of passwords

from PCFGModel import PCFGModel
import sys

def main(filename):	
	model = PCFGModel()
	model.deserializeModel('jumpstart.pkl')
	model.strengthenFile(filename)

if __name__ == "__main__":
	assert len(sys.argv)>=2, "usage: ./jumpstart <filename>"
	main(sys.argv[1])

