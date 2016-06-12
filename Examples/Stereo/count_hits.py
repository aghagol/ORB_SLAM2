log = 'loc_panic_cnn'
filename = 'logs/'+log+'/log.txt'

hit = 0
with open(filename) as f:
	for line in f:
		if not line[:5]=='DEBUG':
			continue
		ss = line.split()
		if ss[4]=='matching':
			hit += {'0':0,'1':1}[ss[-1]]

print "%d hits"%hit
