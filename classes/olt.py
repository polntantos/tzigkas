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
	rounds = 10

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
			window=int(onu.buffer/100)+onu.rtt
			onu.receivePermission(window)
		elif self.algo=='fixed_window':
			window=self.windowSize+onu.rtt
			onu.receivePermission(window)
		elif self.algo=='hybrid':
			window=int(onu.buffer/100)+onu.rtt
			if window>self.windowSize:
				window=self.windowSize+onu.rtt
			onu.receivePermission(window)
		else: #default
			window=int(onu.buffer/100)+onu.rtt
			onu.receivePermission(window)


	def receivePacket(self,onu):
		buffer = onu.transmitBuffer()
		print('remaining buffer for cur onu',onu.getName(),buffer,'transmition time left:',onu.transmit_time_left,sep=' ')
		if buffer<=0 and self.algo!='hybrid':
			new_pack = onu.loadNextPack()

		if self.activeOnu==onu and onu.transmit_time_left<=0:
			if (self.algo=='hybrid') :
				new_pack = self.activeOnu.loadNextPack()
			self.activeOnu=None
			self.nextOnu=None


	def logOnusBuffers(self):
		onusArray = []
		localtime = time.localtime()
		result = time.strftime("%I:%M:%S %p", localtime)
		for onu in Olt.pollingTable:
			onusArray.append(onu.getName()+' '+onu.getBuffer()+' '+onu.getRtt()+' '+onu.getStatus())
			self.stat_line[onu.name]=onu.buffer
		print(*onusArray,result,sep='|')
		self.stat_line['timestamp']=result
		if(self.activeOnu!=None and self.nextOnu!=None):
			print('active Onu:',self.activeOnu.getName(),'next Onu:',self.nextOnu.getName(), sep=' ')
			self.stat_line['active Onu']=self.activeOnu.name
			self.stat_line['next Onu']=self.nextOnu.name
		print(' ')

	def work(self):
		flag=True
		while self.rounds>0:
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
			print(self.stat_line.items())
			# tempValArray = np.array(self.stat_line.values())
			# self.timeSheet.append(tempValArray.copy())
			temparr=copy.deepcopy(self.stat_line)
			self.timeSheet.append(temparr.values())
			self.rounds=self.rounds-1
			# print(self.timeSheet)

		print(self.timeSheet)
		excel=pd.DataFrame(
			self.timeSheet,
			columns=self.stat_line.keys()
		)
		excel.to_excel('output.xlsx')
