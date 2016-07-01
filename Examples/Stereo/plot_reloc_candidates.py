import os,sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

log = 'pioneer_loc'

filename = 'logs/'+log+'/log.txt'

# testpath = '/home/mo/Desktop/ROS_data/jaguar/2016-03-04/test/left/'
# trainpath = '/home/mo/Desktop/ROS_data/jaguar/2016-03-04/train/left/'

testpath = '/home/mo/Desktop/ROS_data/pioneer/2016-04-27/test/left/'
trainpath = '/home/mo/Desktop/ROS_data/pioneer/2016-04-27/train/left/'

outpath = '/home/mo/Desktop/out/'+log+'/'
if not os.path.exists(outpath): os.mkdir(outpath)

def mplot(fig,imfile,cands,suc):
	fig.suptitle('Relocalization successfull? %d'%suc)
	a = fig.add_subplot(5,5,1)
	a.axis('off')
	img = mpimg.imread(testpath+imfile)
	plt.imshow(img, cmap=plt.get_cmap('gray'))
	a.set_title('input')
	counter=5
	for num, cand in enumerate(cands):
		a = fig.add_subplot(5,5,counter+1)
		a.axis('off')
		img = mpimg.imread(trainpath+cand)
		plt.imshow(img, cmap=plt.get_cmap('gray'))
		a.set_title('candidate %d' %(num+1))
		counter+=1
		if counter>=25:
			break
	plt.savefig(outpath+imfile)

idx = 0
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
		if len(ss)>4 and ss[4]=='found':
			image = ss[3][:-1]+'.png'
			get_candids = True
		if len(ss)>4 and ss[4]=='matching':
			idx +=1
			success = {'0':0,'1':1}[ss[-1]]
			figor.clf()
			if not os.path.exists(outpath+image):
				mplot(figor,image,candids,success)
			print 'processed ' + image + ' (no. %d)'%idx


