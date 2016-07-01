import numpy as np
import matplotlib.pyplot as plt

log = 'pioneer_loc'

filename = 'logs/'+log+'/CameraTrajectory_train_test_2016_03_04.txt'
# n1 = 3530
# n2 = 3333

n1 = 5664
n2 = 4826

# n1 = 9760
# n2 = 4826

x = np.zeros(n1+n2)
y = np.zeros(n1+n2)
z = np.zeros(n1+n2)
with open(filename) as f:
	for i, s in enumerate(f):
		x[i] = s.split()[3]
		y[i] = s.split()[7]
		z[i] = s.split()[11]

plt.plot(x[:n1],z[:n1],'bs',linewidth=5)
plt.plot(x[n1:],z[n1:],'r.',linewidth=2)
plt.xlim([-100, 50])
plt.ylim([-50, 100])
plt.savefig(filename[:-4]+'.png')
plt.show()

