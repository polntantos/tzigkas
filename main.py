# importing module
import sys
sys.path.append(".")

from classes.olt import Olt
from classes.onu import Onu

onu1 = Onu("Onu1",[600,200,0,0,0],1)
onu2 = Onu("Onu2",[100,200,300,100,0],2)
onu3 = Onu("Onu3",[300,200,300,0,100],1)
# onu4 = Onu("name4","test4",4)

while True:
    try:
        
        print("1:full_buffer This option allows the onu to transmit it's buffer no matter the size")
        print("2:fixed_window This option allows the onu to transmit it's buffer within the desired window not restricting the window to the buffer's size")
        print("3:hybrid This option calculates the onu's buffer to either restrict the window or provide the maximum allowed size")
        algo = int(input("Please select the desired algorithm [1-3]: "))
        if algo not in (1,2,3):
            print("option ",algo," does not exist please select one of [ 1 2 3 ]")
    except ValueError:
        print("Sorry, I didn't understand that.")
        continue
    else:
        break
    
if(algo==1):
    algo='full_buffer'
elif(algo==2):
    algo='fixed_window'
elif(algo==3):
    algo='hybrid'
    
windowSize=0

if(algo in ('fixed_window','hybrid')):
	while True:
		try:
			windowSize = int(input("Please enter window size in seconds: "))
		except ValueError:
			print("Sorry, I didn't understand that.")
			continue
		else:
			break

olt = Olt('olt1',windowSize,algo)

onusList = [
    onu1,
	onu2,
	onu3,
	# onu4
 ]

for onu in onusList:
    olt.discoverOnu(onu)
    print('discovered',onu.getName()+' '+onu.getBuffer()+' '+onu.getRtt(),sep=' ')

# onu1.logData()
print('OLT working')
olt.work()