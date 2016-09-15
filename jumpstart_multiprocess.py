#!/usr/bin/python

# a jumpstart script to strengthen a file of passwords

from PCFGModel import PCFGModel
import sys,copy,os
import multiprocessing

def strengthenProcess(id, psswds, localmodel):
	#localmodel = copy.copy(model)
	fo = file(str(id)+'.tmp','w')
	print 'Process(pid-'+ str(os.getpid()) +'): temporary file \"'+str(id)+'.tmp'+'\" has been created.'
	count = 0
	for l in psswds:
		if len(l.replace('\n','')) != 0:
			psswd = l.replace('\n','')
			newpsswd = localmodel.strengthen(psswd)
			localmodel.update(psswd,newpsswd)
			count += 1
			if count%100 == 0:
				print 'Process(pid-'+ str(os.getpid()) +'): ' + str(count) + ' passwords strengthened'
			fo.write(newpsswd+'\n')
	fo.close()


def main(filename,n):
	model = PCFGModel()
	model.deserializeModel('jumpstart.pkl')
	print "Trained model loaded..."
	fi = open(filename,'r')
	lines = fi.readlines()
	fi.close()
	assert n < len(lines), "level of parallelism must lower than the number of passwords to be processed!"
	processpool = []
	landmark = [0]
	seglen = len(lines)/n
	for i in range(0,n-1):
		landmark.append(landmark[i]+seglen)
	landmark.append(len(lines))
	for i in range(0,n):
		processpool.append(multiprocessing.Process(name='Worker'+str(i),target=strengthenProcess,args = (i,lines[landmark[i]:landmark[i+1]],model)))
	for t in processpool:
		t.start()
	for i in range(len(processpool)-1,-1,-1):
		if processpool[i].is_alive():
			processpool[i].join()
	fo = open(filename+'.strengthened','w')
	for i in range(0,n):
		fi = open(str(i)+'.tmp','r')
		fo.writelines(fi.readlines())
		fi.close()
		os.remove(str(i)+'.tmp')
		print "Main process: deleted "+str(i)+'.tmp'
	fo.close()


if __name__ == "__main__":
	assert len(sys.argv)>=3, "usage: ./jumpstart_multithread <filename> level_of_parallelism"
	main(sys.argv[1],int(sys.argv[2]))