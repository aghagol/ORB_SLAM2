import matplotlib.pyplot as plt
import numpy as np

# logfiles = ['loc','loc_cnn','loc_panic','loc_panic_cnn','loc_lesschecks_panic_cnn']
# logfiles = ['loc_panic','loc_panic_cnn','loc_lesschecks_panic_cnn']
logfiles = ['loc_panic_nodiscard_minthresh_top10cnn']
# logfiles = ['loc_nochecks_lowthresh_panic_cnn']

for log in logfiles:
	filename = 'logs/'+log+'/log.txt'
	can = []
	ret = []
	hit = []
	ngm = []
	with open(filename) as f:
		for line in f:
			if not line[:5]=='DEBUG':
				continue
			ss = line.split()
			if ss[-1]=='candidates':
				can.append(int(ss[-2]))
			if ss[-1]=='retained':
				ret.append(int(ss[-3]))
			if len(ss)>4 and ss[4]=='matching':
				hit.append({'0':0,'1':1}[ss[-1]])
			if ss[1]=='nGoodMax=':
				ngm.append(int(ss[2]))
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
	ax = fig.add_subplot(1,1,1)
	h1, = ax.plot(np.arange(len(ngm))[np.array(hit)>0],np.array(ngm)[np.array(hit)>0],'bs')
	h2, = ax.plot(np.arange(len(ngm))[np.array(hit)<1],np.array(ngm)[np.array(hit)<1],'r.')
	ax.set_xlabel('frame number (test)')
	ax.set_ylabel('max(nGood)')
	ax.set_xlim([-100, 3400])
	# ax.set_ylim([-1, 11])
	ax.legend([h1,h2],['successful %.2f'%(sr),'failed reloc'],loc='best')
	plt.savefig('logs/'+log+'/nGoodStats_%s.png'%(log))
	plt.close(fig)
