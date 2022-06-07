from multiprocessing.connection import wait
import time


class Onu:
	buffer = 0
	rtt = 1
	buffer = 0
	listOfPackets=[]
	status='idle'
	time_for_answer=0
	transmit_time_left=0
	
	def __init__(self,name,bufferData,rtt):
		self.name = name
		self.listOfPackets = bufferData
		self.rtt = rtt
		if self.listOfPackets:
			self.buffer =  self.listOfPackets.pop(0)
		else:
			self.buffer = 0

	def getName(self):
		return 'Onu_name='+str(self.name)

	def getStatus(self):
		return 'Status='+str(self.status)

	def getBuffer(self):
		return 'Onu_Buffer='+str(self.buffer)

	def getrtt(self):
		return 'rtt='+str(self.rtt)

	def receivePermission(self):
		self.time_for_answer=int(self.rtt)
		self.transmit_time_left=int(self.buffer/100)+self.rtt+1
		self.status='transmitting'

	def transmitBuffer(self):
		self.transmit_time_left-=1
		if self.time_for_answer>0:
			self.time_for_answer-=1
			print('Onu', self.name, 'time for answer:',self.time_for_answer,sep=' ')
			return (self.buffer)
		
		# print('Onu', self.name, 'transmition time left:',self.transmit_time_left,sep=' ')

		if self.buffer>0:
			self.buffer-=100
			if(self.buffer<=0):
				self.buffer=0
				self.status='idle'
			return (self.buffer)
		else:
			self.status='idle'
			return 0

	def loadNextPack(self):
		if self.listOfPackets:
			self.buffer = self.listOfPackets.pop(0)
			return self.buffer
		else:
			return 0