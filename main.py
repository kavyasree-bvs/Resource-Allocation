import os.path
as_str = "aggiestack"
show_str = "show"
config_str = "config"
server_str = "server"
admin_str = "admin"

class machine:
	def __init__(self, name, rackName, ip, mem, numDisks, numCores):
	#def __init__(self, name, ip, mem, numDisks, numCores):
		self.name = name
		self.rackName = rackName
		self.ip = ip
		self.mem = mem #in GB
		self.numDisks = numDisks
		self.numCores = numCores
		self.availableMem = 0
		self.availableDisks = 0
		self.availableCores = 0
	def initAvailableParams(self):
		self.availableCores = self.numCores
		self.availableDisks = self.numDisks
		self.availableMem = self.mem
	def allocateSpace(self, mem, numDisks, numCores):
		self.availableCores -= numCores
		self.availableDisks -= numDisks
		self.availableMem -= mem
	def deallocateSpace(self, mem, numDisks, numCores):
		self.availableCores += numCores
		self.availableDisks += numDisks
		self.availableMem += mem

class rack:
	def __init__(self, name, storagecap):
		self.name =name
		self.storageCapacity = storagecap

class image:
	def __init__(self, imageName, imageSize, imagePath):
	#def __init__(self, imageName, imagePath):
		self.imageName = imageName
		self.imageSize = imageSize #in MB
		self.imagePath = imagePath

class flavor:
	def __init__(self, flavorName, RAM, noOfDisks, noOfVcpus):
		#amount of RAM in GB, the number of disks, the number of vcpus. 
		self.flavorName = flavorName
		self.RAM = RAM #in GB
		self.noOfDisks = noOfDisks
		self.noOfVcpus = noOfVcpus

class instance:
	def __init__(self, instanceName, imageName, flavorName):
		self.instanceName = instanceName
		self.imageName = imageName
		self.flavorName = flavorName
		self.serverHosting = "none"
		self.rack = "none"
	def updateServer(self, server):
		self.serverHosting = server
	def updateRack(self, rack):
		self.rack = rack

racks = []
machines = []
images = []
flavors = []
instances = []

def ReadConfigFile(configFileName):
	with open(configFileName) as f:
		content = f.readlines()
	content = [x.strip() for x in content] 

	curr_index = 0
	noOfRacks = int(content[curr_index])
	
	curr_index +=1
	for n in range(noOfRacks):
		if(len(content[curr_index+n].split()) != 2):
			print 'ERROR: Incorrect format. Should be in <rack name> <storage capacity>'
			return False
		(name, val) = content[curr_index+n].split()
		rh = rack(name,int(val))
		racks.append(rh)
	
	curr_index +=noOfRacks
	noOfMachines = int(content[curr_index])
	curr_index +=1
	
	for n in range(noOfMachines):
		if(len(content[curr_index+n].split()) != 6):
			print 'ERROR: Incorrect format. Should be in <name> <rack name> <ip> <mem> <num-disks> <num-cores>'
			return False
		(name, rackName, ip, mem, numDisks, numCores) = content[curr_index+n].split()
		mh = machine(name, rackName, ip, int(mem), int(numDisks), int(numCores))
		mh.initAvailableParams()
		machines.append(mh)
	return True

def ShowHardware():
	#do error check for len = 0
	#and return fail
	print 'no of racks = ', len(racks)
	for i in range(len(racks)):
		print racks[i].name, racks[i].storageCapacity
	''''''
	print 'no of machines = ', len(machines)
	for i in range(len(machines)):
		print machines[i].name, machines[i].rackName, machines[i].ip, machines[i].mem, machines[i].numDisks, machines[i].numCores
	return True

def ShowCurrentlyAvailableHardware():
	if(len(machines)==0):
		print 'No machines to show'
		return True
	print 'no of currently available machines = ', len(machines)
	for i in range(len(machines)):
		print machines[i].name, machines[i].availableMem, machines[i].availableDisks, machines[i].availableCores
	return True

def ReadImageFile(configFileName):
	with open(configFileName) as f:
		content = f.readlines()
	content = [x.strip() for x in content] 

	curr_index = 0
	noOfImages = int(content[0])
	
	curr_index +=1
	for n in range(noOfImages):
		if(len(content[curr_index+n].split()) != 3):
			print 'ERROR: Incorrect format. Should be in <image name> <size> <path>'
			return False

		(name, size, path) = content[curr_index+n].split()
		im = image(name,int(size),path)
		images.append(im)
	return True

def ShowImages():
	print 'no of images = ', len(images)
	for i in range(len(images)):
		print images[i].imageName, images[i].imageSize, images[i].imagePath

def ReadFlavorFile(configFileName):
	with open(configFileName) as f:
		content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content] 
	#print content

	curr_index = 0
	noOfFlavors = int(content[0])
	#print noOfFlavors
	
	curr_index +=1
	for n in range(noOfFlavors):
		if(len(content[curr_index+n].split()) != 4):
			print 'ERROR: Incorrect format. Should be in <flavor name> <size> <disks> <vcpus>'
			return False
		(name, size, disks, vcpus) = content[curr_index+n].split()
		fl = flavor(name,int(size),int(disks), int(vcpus))
		flavors.append(fl)
	return True

def ShowFlavors():
	print 'no of flavors = ', len(flavors)
	for i in range(len(flavors)):
		print flavors[i].flavorName, flavors[i].RAM, flavors[i].noOfDisks, flavors[i].noOfVcpus

def FindMachineIndex(machineName):
	for i in range(len(machines)):
		curr = machines[i]
		if(curr.name == machineName):
			return i
	return -1

def FindFlavorIndex(flavorType):
	for i in range(len(flavors)):
		curr = flavors[i]
		if(curr.flavorName == flavorType):
			return i
	return -1

def FindInstanceIndex(name):

	for i in range(len(instances)):
		curr = instances[i]
		if(curr.instanceName == name):
			return i
	return -1

def FindRackIndex(name):
	for i in range(len(racks)):
		curr = racks[i]
		if(curr.name == name):
			return i
	return -1

def IsSpaceAvail(a,b):
	if(a>=b):
		return True
	return False

def CanHost(machineName, flavorType):
	machineIndex = FindMachineIndex(machineName)
	if(machineIndex == -1):
		print 'ERROR: no machine of given name found'
		return
	flavorIndex = FindFlavorIndex(flavorType)
	if(flavorIndex == -1):
		print 'ERROR: no flavor of given name found'
		return
	#print machineIndex, flavorIndex

	if(IsSpaceAvail(machines[machineIndex].availableMem, flavors[flavorIndex].RAM) and IsSpaceAvail(machines[machineIndex].availableDisks, flavors[flavorIndex].noOfDisks) and IsSpaceAvail(machines[machineIndex].availableCores, flavors[flavorIndex].noOfVcpus)):
		return True
	return False

def CreateInstance(instancename, imageToBeBootedFrom, flavorname):
	if(len(machines)==0):
		print 'ERROR: no physical servers to host on'
		return False
	for i in range(len(machines)):
		currMach = machines[i].name
		ret = CanHost(currMach, flavorname)
		if(ret):
			flavorIndex = FindFlavorIndex(flavorname)
			if(flavorIndex == -1):
				print 'ERROR: no flavor of given name found'
				return
			currflav = flavors[flavorIndex]
			machines[i].allocateSpace(currflav.RAM, currflav.noOfDisks, currflav.noOfVcpus)
			ins = instance(instancename, imageToBeBootedFrom, flavorname)
			ins.updateServer(currMach)
			ins.updateRack(machines[i].rackName)
			instances.append(ins)

			return True
	print 'ERROR: no free servers'
	return False

def ListInstances():
	if(len(instances)==0):
		print 'ERROR: no instances to list'
		return False
	print len(instances)
	for i in range(len(instances)):
		print instances[i].instanceName, instances[i].imageName, instances[i].flavorName
	return True

def ShowServersOfInstances():
	if(len(instances)==0):
		print 'no instances to show'
		return True
	print 'no of instances = ', len(instances)
	for i in range(len(instances)):
		print instances[i].instanceName, instances[i].serverHosting
	return True

def DeleteInstance(name):
	index = FindInstanceIndex(name)
	if(index == -1):
		print 'ERROR: no instance of given name found'
		return False
	#print 'index is: ', index
	#deallocate the resources and delete the instance
	ins = instances[index]
	flaname = ins.flavorName
	server = ins.serverHosting
	index = FindMachineIndex(server)
	if(index == -1):
		print 'ERROR: no such server is found'
		return False
	flaindex = FindFlavorIndex(flaname)
	if(flaindex == -1):
		print 'ERROR: no flavor of given name found'
		return False
	currflav = flavors[flaindex]
	machines[index].deallocateSpace(currflav.RAM, currflav.noOfDisks, currflav.noOfVcpus)
	#del instances[index]
	
	if(len(instances) == 1):
		instances.pop()
	else:
		instances.pop(index)
	return True

def EvacuateRack(evacname):
	#remove the instances from the current servers on the sick rack
	#delete the servers
	#reallocate the instance to another server on a healthy rack
	# should the rack be deleted as well
	if(len(racks)==0):
		print 'ERROR: no racks to evacuate'
		return True
	index = FindRackIndex(evacname)
	if(index==-1):
		print 'ERROR: no rack of given name found'
		return False
	migratedList = []
	for i in range(len(instances)):
		ins = instances[i]
		if(ins.rack == evacname):
			#print 'ins on rack to be evacuated is: ', ins.instanceName
			migratedList.append(i)
			#remove from existing server
			flaname = ins.flavorName
			serverindex = FindMachineIndex(ins.serverHosting)
			flaindex = FindFlavorIndex(flaname)
			currflav = flavors[flaindex]
			machines[serverindex].deallocateSpace(currflav.RAM, currflav.noOfDisks, currflav.noOfVcpus)
		else:
			continue

	#delete the machines
	machlist = []
	for i in range(0,len(machines)):
		currMach = machines[i].name
		if(machines[i].rackName == evacname):
			machlist.append(i)

	for i in range(0,len(machlist)):
		tempindex = len(machlist) - i - 1
		if(len(machines) == 1):
			machines.pop()
		else:
			machines.pop(machlist[tempindex])

	#reallocate
	for j in range(len(migratedList)):
		ins = instances[j]
		flaname = ins.flavorName
		for i in range(len(machines)):
			currMach = machines[i].name
			ret = CanHost(currMach, flaname)
			if(ret):
				flavorIndex = FindFlavorIndex(flaname)
				if(flavorIndex == -1):
					print 'ERROR: no flavor of given name found'
					return False
				currflav = flavors[flavorIndex]
				machines[i].allocateSpace(currflav.RAM, currflav.noOfDisks, currflav.noOfVcpus)
				ins.updateServer(currMach)
				ins.updateRack(machines[i].rackName)
				break
			if(i == len(machines)-1):
					print 'No free space in any machine to allocate'
	return True


def RemoveMachine(remMachName):
	index = FindMachineIndex(remMachName)
	if(index==-1):
		print 'ERROR: no machine of given name found'
		return False
	migratedList = []
	for i in range(len(instances)):
		ins = instances[i]
		if(ins.serverHosting == remMachName):
			migratedList.append(i)
			#remove from existing server
			flaname = ins.flavorName
			serverindex = FindMachineIndex(ins.serverHosting)
			flaindex = FindFlavorIndex(flaname)
			currflav = flavors[flaindex]
			machines[serverindex].deallocateSpace(currflav.RAM, currflav.noOfDisks, currflav.noOfVcpus)
		else:
			continue
	#delete the machine
	if(len(machines) == 1):
		machines.pop()
	else:
		machines.pop(index)
	#reallocate
	for j in range(len(migratedList)):
		ins = instances[j]
		flaname = ins.flavorName
		for i in range(len(machines)):
			currMach = machines[i].name
			ret = CanHost(currMach, flaname)
			if(ret):
				flavorIndex = FindFlavorIndex(flaname)
				if(flavorIndex == -1):
					print 'ERROR: no flavor of given name found'
					return
				currflav = flavors[flavorIndex]
				machines[i].allocateSpace(currflav.RAM, currflav.noOfDisks, currflav.noOfVcpus)
				ins.updateServer(currMach)
				ins.updateRack(machines[i].rackName)
				break
			else:
				if(i == len(machines)-1):
					print 'No free space in any machine to allocate'
	return True

def AddMachine(mem, disk, vcpus, ip, rack, machineName):
	#adding a new machine
	mh = machine(machineName, rack, ip, int(mem), int(disk), int(vcpus))
	mh.initAvailableParams()
	machines.append(mh)
	return True

	
import datetime

time = 'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
print time
#print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))


log = open('aggiestack-log.txt', 'a')
log.write('\n%s\n'%time)
#log.write()
#write time stamp and start logging
def logOutput(ret):
	if(ret):
		log.write('%s\n'%SUC_STR)
	else:
		log.write('%s\n'%FAIL_STR)

SUC_STR = "SUCCESS"	
FAIL_STR = "FAILURE"


while True:
	try:
		cmd =raw_input()
		log.write('%s\n'%cmd)
		cmd_parts = cmd.split()
		if(len(cmd_parts)==0):
			continue

		if(cmd_parts[0] != as_str):
			print "ERROR: Incorrect format. cmd should begin with", as_str
			log.write('%s\n'%FAIL_STR)
			continue
		
		if(cmd_parts[1] == show_str):
			#do error check for len = 0
			#and return fail
			if(cmd_parts[2]=="hardware"):
				ret = ShowHardware()
				logOutput(ret)
			elif(cmd_parts[2]=="images"):
				ShowImages()
				logOutput(True)
			elif(cmd_parts[2]=="flavors"):
				ShowFlavors()
				logOutput(True)
			elif(cmd_parts[2]=="all"):
				ShowHardware()
				ShowImages()
				ShowFlavors()
				logOutput(True)
			else:
				print "ERROR: Invalid parameters. Can show hardware/images/flavor/all"
				logOutput(False)
		
		elif(cmd_parts[1]==config_str):
			if(cmd_parts[2]== "--hardware"):
				fname = cmd_parts[3]
				if(os.path.isfile(fname) == False):
					print "ERROR: File does not exist"
					logOutput(False)
				else:
					ret = ReadConfigFile(fname)
					logOutput(ret)
			elif(cmd_parts[2]=="--images"):
				fname = cmd_parts[3]
				if(os.path.isfile(fname) == False):
					print "ERROR: File does not exist"
					logOutput(False)
				else:
					ret = ReadImageFile(fname)
					logOutput(ret)
			elif(cmd_parts[2]=="--flavors"):
				fname = cmd_parts[3]
				if(os.path.isfile(fname) == False):
					print "ERROR: File does not exist"
					logOutput(False)
				else:
					ret = ReadFlavorFile(fname)
					logOutput(ret)
			else:
				print 'ERROR: Invalid parameters. Can config only hardware/flavors/images'
				logOutput(False)

		elif(cmd_parts[1] == server_str):
			#print "server case"
			if(cmd_parts[2]=="create"):
				if(cmd_parts[3]=="--image" and cmd_parts[5]=="--flavor"):
					imageToBeBootedFrom = cmd_parts[4]
					flavor_name = cmd_parts[6]
					instance_name = cmd_parts[7]
					ret = CreateInstance(instance_name, imageToBeBootedFrom, flavor_name)
					logOutput(ret)
			elif(cmd_parts[2]=="list"):
				ret = ListInstances()
				logOutput(ret)
			elif(cmd_parts[2]=="delete"):
				ret = DeleteInstance(cmd_parts[3])
				logOutput(ret)
			else:
				print "Invalid command"
				logOutput(False)

		elif(cmd_parts[1] == admin_str):
			if(cmd_parts[2]== "show"):
				if(cmd_parts[3]=="hardware"):
					ret = ShowCurrentlyAvailableHardware()
					logOutput(ret)
				elif(cmd_parts[3]=="instances"):
					ret = ShowServersOfInstances()
					logOutput(ret)
			elif(cmd_parts[2]=="can_host"):
				machineName = cmd_parts[3]
				flavorType = cmd_parts[4]
				ret = CanHost(machineName, flavorType)
				if(ret):
					print "yes"
				else:
					print "no"
			elif(cmd_parts[2]=="evacuate"):
				ret = EvacuateRack(cmd_parts[3])
				logOutput(ret)
			elif(cmd_parts[2]=="remove"):
				ret = RemoveMachine(cmd_parts[3])
				logOutput(ret)
			elif(cmd_parts[2]=="add"):
				#check if enough arguments are there
				if(len(cmd_parts)!= 14):
					print 'ERROR: few params to parse'
					logOutput(False)
					continue
				if(cmd_parts[3]=="-mem" and cmd_parts[5]=='-disk' and cmd_parts[7]=='-vcpus' and cmd_parts[9]=='-ip' and cmd_parts[11]=='-rack'):
					AddMachine(cmd_parts[4], cmd_parts[6], cmd_parts[8], cmd_parts[10], cmd_parts[12], cmd_parts[13])
				else:
					print 'incorrect format'
					logOutput(False)
			else:
				print "Invalid command"
				logOutput(False)

		else:
			print "Invalid command"
			logOutput(False)

		continue
	except KeyboardInterrupt:
		log.close()
		print "Terminating CLI .. "
		break