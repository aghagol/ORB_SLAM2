

# logfiles = ['loc','loc_cnn','loc_panic','loc_panic_cnn','loc_lesschecks_panic_cnn']
logfiles = ['loc_panic','loc_panic_cnn','loc_lesschecks_panic_cnn']

for log in logfiles:
	filename = 'logs/'+log+'/log.txt'
	hit = 0
	tot = 0
	with open(filename) as f:
		for line in f:
			if not line[:5]=='DEBUG':
				continue
			ss = line.split()
			if ss[4]=='matching':
				hit += {'0':0,'1':1}[ss[-1]]
				tot += 1
	print "%f success ratio for %s"%(float(hit)/tot,log)
