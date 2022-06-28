import time
import pandas as pd # excel reading
import numpy as np
import copy

from classes.onu import Onu

class Olt:
	pollingTable = []
	activeOnu = None
	nextOnu = None
	windowSize = None
	stat_line={}
	timeSheet=[]
	rounds = 100

	def __init__(self,name,windowSize=10,algo='full_buffer'):
		self.name = name
		self.windowSize = windowSize
		self.algo = algo

	def discoverOnu(self,onu):
		Olt.pollingTable.append(onu)
	
	def forgetOnu(self,onu):
		Olt.pollingTable.remove(onu)
	
	def grant(self,onu):
    #here add an if to check which type of algo you are going to use
    #full packet grant self.transmit_time_left=
		if self.algo=='full_buffer':
			window=int(onu.buffer/100)+int(onu.rtt)
			onu.receivePermission(window)
		elif self.algo=='fixed_window':
			window=self.windowSize+int(onu.rtt)
			onu.receivePermission(window)
		elif self.algo=='hybrid':
			window=int(onu.buffer/100)+int(onu.rtt)
			if window>self.windowSize:
				window=self.windowSize+onu.rtt
			onu.receivePermission(window)
		else: #default
			window=int(onu.buffer/100)+onu.rtt
			onu.receivePermission(window)


	def receivePacket(self,onu):
		buffer = onu.transmitBuffer()
		# print('remaining buffer for cur onu',onu.getName(),buffer,'transmition time left:',onu.transmit_time_left,sep=' ')
		if buffer<=0 and self.algo!='hybrid':
			new_pack = onu.loadNextPack()

		if self.activeOnu==onu and onu.transmit_time_left<=0:
			if (self.algo=='hybrid') or (self.algo=='fixed_window'):
				new_pack = self.activeOnu.loadNextPack()
			self.setOnus()

	def setOnus(self):
		if self.nextOnu==None and self.pollingTable:
			self.activeOnu=self.pollingTable[0]
			self.nextOnu=self.pollingTable[1]
		else:
			self.activeOnu=self.nextOnu
			if self.activeOnu==self.pollingTable[-1]:
				self.nextOnu=self.pollingTable[0]
			else:
				index = self.pollingTable.index(self.activeOnu)
				self.nextOnu=self.pollingTable[index+1]
			self.receivePacket(self.activeOnu)

	def logOnusBuffers(self):
		onusArray = []
		localtime = time.localtime()
		result = time.strftime("%I:%M:%S %p", localtime)
		for onu in Olt.pollingTable:
			onusArray.append(onu.getName()+' '+onu.getBuffer()+' '+onu.getRtt()+' '+onu.getStatus())
			self.stat_line[onu.name]=onu.buffer
			self.stat_line[onu.name+' status']=onu.status
			self.stat_line[onu.name+' time_for_answer']=onu.time_for_answer
			self.stat_line[onu.name+' transmit_time_left']=onu.transmit_time_left
		print(*onusArray,result,sep='|')
		self.stat_line['timestamp']=result
		if(self.activeOnu!=None and self.nextOnu!=None):
			print('active Onu:',self.activeOnu.getName(),'next Onu:',self.nextOnu.getName(), sep=' ')
			self.stat_line['active Onu']=self.activeOnu.name
			self.stat_line['next Onu']=self.nextOnu.name
		print(' ')

	def work(self):
		# flag=True
		while self.rounds>0:

			if self.activeOnu==None:
				self.setOnus()

			if self.activeOnu!=None:
				if(self.activeOnu.status=='idle'):
					self.grant(self.activeOnu)
				else:
					self.receivePacket(self.activeOnu)
			
			if((self.nextOnu.status=='idle') and (self.activeOnu.transmit_time_left<=self.nextOnu.rtt)):
				self.grant(self.nextOnu)
			elif (self.activeOnu.transmit_time_left<=self.nextOnu.rtt):
				self.receivePacket(self.nextOnu)
			
			# print(self.stat_line.items())
			Olt.logOnusBuffers(self)
			
			temparr=copy.deepcopy(self.stat_line)
			self.timeSheet.append(temparr.values())
			self.rounds=self.rounds-1

		# print(self.timeSheet)
		excel=pd.DataFrame(
			self.timeSheet,
			columns=self.stat_line.keys()
		)
		excel.to_excel('output.xlsx')
