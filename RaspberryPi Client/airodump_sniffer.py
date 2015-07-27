import subprocess
import signal
import time

def start_mon(iface):
	
	subprocess.call(["ifconfig", iface, "down"])
	subprocess.call(["iwconfig", iface, "mode", "monitor"])
	subprocess.call(["ifconfig", iface, "up"])
	print "Starting Monitor mode on", iface+"."
	
	return iface
	
def stop_mon(mon_iface):
	
	subprocess.call(["ifconfig", mon_iface, "down"])
	subprocess.call(["iwconfig", mon_iface, "mode", "managed"])
	subprocess.call(["ifconfig", mon_iface, "up"])
	print "Monitor mode on", mon_iface, "stopped."

def get_mon_iface():

	iwconfig_getmon = subprocess.Popen(["iwconfig"], stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
	
	for line in iwconfig_getmon.stdout: #Scan through every line
		
		if (line[0:5].strip(" \t\n\r") is not ""):
			current_iface = line[0:5].strip(" \t\n\r")
			
		if line.find("Monitor") >= 0:
			mon_iface = current_iface
			print "Monitor Interface found on", mon_iface+"."
			break
			
		elif line.find("Managed") >= 0:
			print "Monitor Interface not found."
			mon_iface = start_mon(current_iface)
			break
	
	return mon_iface
	
def start_sniff(mon_iface, timeout):
	
	data_list = []
	data = []
	bssid_count = 0
	
	print "Starting Sniff on", mon_iface, "for", timeout ,"seconds."
	
	airodump = subprocess.Popen(['airodump-ng', mon_iface], stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE, universal_newlines = True)
	airodump.stdin.write('aa')
	
	time.sleep(timeout) #Wait for specified time.
	airodump.kill() #Kill Airodump-ng process
	
	
	print "Scan Stopped."
	
	for line in airodump.stderr:
		
		line = line.strip(" \n")
		
		try:
			if line[2] is ':':
				data = line.split()
				data_list.append(data)
				bssid_count += 1
				
		except:
			pass #Ignore error.
		
		if line.find("\x1b[1;1H") >= 0:
			data_list = []
			bssid_count = 0
	print "Number of networks found:", bssid_count
	return data_list
	
mon_iface = get_mon_iface()

cell_table = start_sniff(mon_iface, 5)

for line in cell_table:
	print line
#stop_mon(mon_iface)