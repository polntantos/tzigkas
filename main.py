# importing module
import sys
sys.path.append(".")

from classes.olt import Olt
from classes.onu import Onu

onu1 = Onu("Onu1",[600,500,0,0,0],3)
onu2 = Onu("Onu2",[700,500,300,100,0],2)
onu3 = Onu("Onu3",[700,200,300,0,100],4)
# onu4 = Onu("name4","test4",4)

olt = Olt('olt1')

onusList = [
    onu1,
	onu2,
	onu3,
	# onu4
 ]

for onu in onusList:
    olt.discoverOnu(onu)
    print('discovered',onu.getName()+' '+onu.getBuffer()+' '+onu.getrtt(),sep=' ')

# onu1.logData()
print('OLT working')
olt.work()