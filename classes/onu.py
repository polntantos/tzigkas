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
		return 'Name='+str(self.name)

	def getStatus(self):
		return 'Status='+str(self.status)

	def getBuffer(self):
		return 'Buffer='+str(self.buffer)

	def getRtt(self):
		return 'rtt='+str(self.rtt)

	def receivePermission(self,windowSize):
		self.time_for_answer=int(self.rtt)
		if(windowSize > 0):
			self.transmit_time_left=windowSize+1
			self.status='transmitting'
			return 1;
		else:
			return 0;

	def transmitBuffer(self):
		self.transmit_time_left-=1
		if self.time_for_answer>0:
			self.time_for_answer-=1
			print('Onu', self.name, 'time for answer:',self.time_for_answer,sep=' ')
			return (self.buffer)
		
		# print('Onu', self.name, 'transmition time left:',self.transmit_time_left,sep=' ')

		if self.transmit_time_left>=1:
			self.buffer-=100
			if(self.buffer<=0):
				self.buffer=0
		else:
			self.status='idle'
			
		return (self.buffer)

	def loadNextPack(self):
		if self.listOfPackets:
			self.buffer = self.listOfPackets.pop(0)
			return self.buffer
		else:
			return 0