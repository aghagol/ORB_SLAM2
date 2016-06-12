import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

log = 'loc_lesschecks_panic_cnn'
filename = 'logs/'+log+'/log.txt'

testpath = '/home/mo/Desktop/ROS_data/jaguar/2016-03-04/test/left/'
trainpath = '/home/mo/Desktop/ROS_data/jaguar/2016-03-04/train/left/'
outpath = '/home/mo/Desktop/out/'+log+'/'

def mplot(fig,imfile,cands,suc):
	fig.suptitle('Relocalization successfull? %d'%suc)
	a = fig.add_subplot(5,6,1)
	img = mpimg.imread(testpath+imfile)
	plt.imshow(img, cmap=plt.get_cmap('gray'))
	a.set_title('input')
	counter=1
	for cand in cands:
		a = fig.add_subplot(5,6,counter+1)
		img = mpimg.imread(trainpath+cand)
		plt.imshow(img, cmap=plt.get_cmap('gray'))
		a.set_title('candidate %d' %counter)
		counter+=1
		if counter>=30:
			break
	plt.savefig(outpath+imfile)

figor = plt.figure(figsize=(20,10))
get_candids = False
with open(filename) as f:
	for line in f:
		if (not line[:5]=='DEBUG') and (not get_candids):
			continue
		ss = line.split()
		if get_candids:
			candids = [ent+'.png' for ent in ss]
			get_candids = False
			continue
		if ss[4]=='found':
			image = ss[3][:-1]+'.png'
			get_candids = True
		if ss[4]=='matching':
			success = {'0':0,'1':1}[ss[-1]]
			figor.clf()
			if not os.path.exists(outpath+image):
				mplot(figor,image,candids,success)
			print 'processed ' + image


