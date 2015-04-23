#!/usr/bin/env python
#uses 3 replicates of tab delimited files of mass and intensity and
#organize it by categories placed by the minor values plus error
#usage: python mass_merge.py replicate1 replicate2 replicate3 outputfile

#make_groups and organize_write can be improved

from sys import argv
from collections import OrderedDict


def read_replicate(infile, ch):
	"""read the replicate file and return it in a ordered dic in the
	following way: mass(key)=intensity(value)"""
	rep=open(infile)
	rep.readline()
	dic=OrderedDict()
	for i in rep:
		line=i.split()
		dic[float(line[0])]=ch+line[1].strip()
	rep.close()
	return dic

def error_calc(theoric_mass):
	"""calc the error and the value to be compared  
	in the group formation and return it"""
	errorr=theoric_mass/1000000#change to acept diferent ppms
	compare=theoric_mass+errorr
	return compare

def make_groups(rep1,rep2,rep3):#change to acept a variable number of replicates
	"""iterate by the lists and make sets by the compare value from
	error_calc. returns a dictionary with the mean value and the intensity
	from each replicate"""
	repl1=read_replicate(rep1,"a")
	repl2=read_replicate(rep2,"b")
	repl3=read_replicate(rep3,"c")
	temp=[]
	final={}
	la=repl1.keys()
	la+=repl2.keys()
	la+=repl3.keys()
	l=list(set(la))
	l.sort()
	last=l[-1]
	for el in l:
		if not temp:
			compare=error_calc(el)
			temp=[el]
		else:
			if el<compare:
				temp.append(el)
			if el > compare or el==last:
				mean=sum(temp)/float(len(temp))
				final[mean]=[]
				for g in temp:
					if g in repl1:
						final[mean].append(repl1[g])
					if g in repl2:
						final[mean].append(repl2[g])
					if g in repl3:
						final[mean].append(repl3[g])
				temp=[]				
				compare=error_calc(el)
				temp=[el]
	return final

def organize_write(dic, outfile):
	"""organize the dictionary returned by make_groups and write it to 
	a file"""
	t=""
	temp=["0\t","0\t","0\n"]
	out=open(outfile,"w")
	out.write("mass_average\treplicate1\treplicate2\treplicate3\n")
	for key, value in dic.items():
		for el in value:
			if el.startswith("a"):
				temp[0]=el[1:]+"\t"
			elif el.startswith("b"):
				temp[1]=el[1:]+"\t"
			elif el.startswith("c"):
				temp[2]=el[1:]+"\n"
		for i in temp:
			t+=i
		out.write(str(key)+"\t")
		out.write(t)
		temp=["0\t","0\t","0\n"]
		t=""
	out.close()
	
		

organize_write(make_groups(argv[1],argv[2], argv[3]), argv[4])
