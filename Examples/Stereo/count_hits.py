import matplotlib.pyplot as plt
import numpy as np

logfiles = ['tmp']

for log in logfiles:
	filename = 'logs/'+log+'/log.txt'
	can = []
	ret = []
	hit = []
	nm = []
	ng = []
	with open(filename) as f:
		for line in f:
			if not line.strip(): continue
			ss = line.split()
			if line[:5]=='DEBUG':
				if ss[-1]=='candidates':
					can.append(int(ss[-2]))
				if ss[-1]=='retained':
					ret.append(int(ss[-3]))
				if len(ss)>4 and ss[4]=='matching':
					hit.append({'0':0,'1':1}[ss[-1]])
				continue
			if ss[0]=='nmatches:':
				nm.append([int(i.split('->')[1]) for i in ss[1:]])
			if ss[0]=='nGood:':
				ng.append([int(i) for i in ss[1:]])

	sr = float(sum(hit))/len(hit)
	print "%f success ratio for %s"%(sr,log)

	fig = plt.figure(figsize=(20,10))
	ax = fig.add_subplot(1,1,1)
	h1, = ax.plot(np.arange(len(ret))[np.array(hit)>0],np.array(ret)[np.array(hit)>0],'bs')
	h2, = ax.plot(np.arange(len(ret))[np.array(hit)<1],np.array(ret)[np.array(hit)<1],'r.')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('number of retained candidates')
	ax.set_xlim([-100, 3400])
	ax.set_ylim([-1, 11])
	ax.legend([h1,h2],['successful %.2f'%(sr),'failed reloc'],loc='best')
	plt.savefig('logs/'+log+'/CandidateStats_%s.png'%(log))
	plt.close(fig)

	fig = plt.figure(figsize=(20,10))
	fig.suptitle('%d percent zeros'%(np.count_nonzero(np.array(ng))/10./len(ng)*100))
	ax = fig.add_subplot(1,1,1)
	hit_idx = np.arange(len(hit))[np.array(hit)>0]
	mis_idx = np.arange(len(hit))[np.array(hit)<1]
	for i in range(10):
		ax.plot(hit_idx,np.array(ng)[hit_idx][:,i],'bs')
		ax.plot(mis_idx,np.array(ng)[mis_idx][:,i],'r.')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('nGood (for every candidate per test frame)')
	ax.set_xlim([-100, 3400])
	plt.savefig('logs/'+log+'/nGoodStats_%s.png'%(log))
	plt.close(fig)

	fig = plt.figure(figsize=(20,10))
	ax = fig.add_subplot(1,1,1)
	for i in range(10):
		ax.plot(range(len(nm)),np.array(nm)[:,i],'bs')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('nMatches (for every candidate per test frame)')
	ax.set_xlim([-100, 3400])
	plt.savefig('logs/'+log+'/nMatchStats_%s.png'%(log))
	plt.close(fig)
