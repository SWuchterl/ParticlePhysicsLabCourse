import numpy as np
import matplotlib.pyplot as plt

ar_A=[]
ar_B=[]
ar_erA=[]
ar_erB=[]
ar_A_without=[]
ar_B_without=[]
ar_erA_without=[]
ar_erB_without=[]
ar_i=[]

for i in range(10,200,10):
    temp=np.loadtxt("values/cali"+str(i)+".txt",skiprows=0)
    ar_A.append(temp[0])
    ar_B.append(temp[2])
    ar_erA.append(np.sqrt(temp[1]))
    ar_erB.append(np.sqrt(temp[3]))
    ar_A_without.append(temp[4])
    ar_B_without.append(temp[6])
    ar_erA_without.append(np.sqrt(temp[5]))
    ar_erB_without.append(np.sqrt(temp[7]))
    ar_i.append(i)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.set_title("slope a")
ax1.errorbar(ar_i,ar_A,yerr=ar_erA,fmt=".")
ax1.errorbar(ar_i,ar_A_without,yerr=ar_erA_without,fmt=".")
plt.xlabel("n Bins")
ax2 = fig.add_subplot(212, sharex=ax1)
ax2.set_title("intercept b")
ax2.errorbar(ar_i,ar_B,yerr=ar_erB,fmt=".")
ax2.errorbar(ar_i,ar_B_without,yerr=ar_erB_without,fmt=".")
plt.xlabel("n Bins")
plt.subplots_adjust(hspace=0.5, wspace=1.0)
# plt.show()
plt.savefig("systematics.pdf")
