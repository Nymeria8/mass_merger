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

def make_groups(rep1,rep2,rep3):
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
	for el in l:
		if not temp:
			compare=error_calc(el)
			temp=[el]
		else:
			if el<compare:
				temp.append(el)
			else:
				mean=sum(temp)/float(len(temp))
				final[mean]=[]
				for g in temp:
					if g in repl1:
						final[mean].append(repl1[g])
					elif g in repl2:
						final[mean].append(repl2[g])
					elif g in repl3:
						final[mean].append(repl3[g])
				temp=[]				
				compare=error_calc(el)
	return final

def organize_write(dic, outfile):
	"""organize the dictionary returned by make_groups and write it to 
	a file"""
	#print(dic)
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
		print(str(key))
		out.write(str(key)+"\t")
		out.write(t)
		temp=["0\t","0\t","0\n"]
		t=""
	out.close()
	
		

organize_write(make_groups(argv[1],argv[2], argv[3]), argv[4])
