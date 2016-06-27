import matplotlib.pyplot as plt
import numpy as np

logfiles = ['nkp']

for log in logfiles:
	filename = 'logs/'+log+'/log.txt'
	can = []
	ret = []
	hit = []
	nm = []
	ng = []
	nkp = []
	nkp_can = []
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
				if len(ss)>1 and ss[1]=='N':
					nkp.append(int(ss[2]))
					nkp_can.append([int(i.split('->')[1]) for i in ss[3:]])
				continue
			if ss[0]=='nmatches:':
				nm.append([int(i.split('->')[1]) for i in ss[1:]])
			if ss[0]=='nGood:':
				ng.append([int(i) for i in ss[1:]])

	hit_idx = np.arange(len(hit))[np.array(hit)>0]
	mis_idx = np.arange(len(hit))[np.array(hit)<1]
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
	ax.grid(True)
	plt.savefig('logs/'+log+'/CandidateStats_%s.png'%(log))
	plt.close(fig)

	fig = plt.figure(figsize=(20,10))
	ng = np.array(ng)
	fig.suptitle('%d %% PnP failure'%(float((ng[mis_idx]==-50).sum())/(ng[mis_idx].size)*100))
	ax = fig.add_subplot(1,1,1)
	for i in range(10):
		ax.plot(hit_idx,ng[hit_idx][:,i],'bs')
		ax.plot(mis_idx,ng[mis_idx][:,i],'r.')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('nGood (for every candidate per test frame)')
	ax.set_xlim([-100, 3400])
	ax.grid(True)
	plt.savefig('logs/'+log+'/nGoodStats_%s.png'%(log))
	plt.close(fig)

	fig = plt.figure(figsize=(20,10))
	ax = fig.add_subplot(1,1,1)
	for i in range(10):
		ax.plot(range(len(nm)),np.array(nm)[:,i],'bs')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('nMatches (for every candidate per test frame)')
	ax.set_xlim([-100, 3400])
	ax.grid(True)
	plt.savefig('logs/'+log+'/nMatchStats_%s.png'%(log))
	plt.close(fig)

	fig = plt.figure(figsize=(20,10))
	ax = fig.add_subplot(1,1,1)
	for i in range(10):
		ax.plot(range(len(nkp)),np.array(nkp_can)[:,i],'bs')
	ax.plot(range(len(nkp)),nkp,'r')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('number of keypoints')
	ax.set_xlim([-100, 3400])
	ax.grid(True)
	plt.savefig('logs/'+log+'/nStats_%s.png'%(log))
	plt.close(fig)
