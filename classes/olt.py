import time

from classes.onu import Onu

class Olt:
	pollingTable = []
	activeOnu = None
	nextOnu = None

	def __init__(self,name):
		self.name = name

	def discoverOnu(self,onu):
		Olt.pollingTable.append(onu)
		
	def forgetOnu(self,onu):
		Olt.pollingTable.remove(onu)
	
	def grant(self,onu):
		onu.receivePermission()

	def receivePacket(self,onu):
		buffer = onu.transmitBuffer()
		print('remaining buffer for cur onu',onu.getName(),buffer,'transmition time left:',onu.transmit_time_left,sep=' ')
		if buffer<=0:
			onu.loadNextPack()
			if self.activeOnu==onu:
				self.activeOnu=None
				self.nextOnu=None

	def logOnusBuffers(self):
		onusArray = []
		localtime = time.localtime()
		result = time.strftime("%I:%M:%S %p", localtime)
		for onu in Olt.pollingTable:
			onusArray.append(onu.getName()+' '+onu.getBuffer()+' '+onu.getrtt()+' '+onu.getStatus())
		print(*onusArray,result,sep='|')
		if(self.activeOnu!=None and self.nextOnu!=None):
			print('active Onu:',self.activeOnu.getName(),'next Onu:',self.nextOnu.getName(), sep=' ')
		print(' ')

	def work(self):
		flag=True
		while flag:
			# cur_second = int (time.time())
			Olt.logOnusBuffers(self)
			for onu in Olt.pollingTable:
				# print(Olt.pollingTable)
				if self.activeOnu==None:
					self.activeOnu=onu
				
				if self.nextOnu==None:
					if onu != self.activeOnu:
						self.nextOnu=onu
    
				if self.activeOnu==onu:
					if(onu.status=='idle'):
						self.grant(onu)
					else:
						self.receivePacket(onu)

				if self.nextOnu==onu and self.activeOnu!=None:
					if((onu.status=='idle') and (self.activeOnu.transmit_time_left<=self.nextOnu.rtt)):
						self.grant(onu)
					elif (self.activeOnu.transmit_time_left<=self.nextOnu.rtt):
						self.receivePacket(onu)
			time.sleep(1)
			