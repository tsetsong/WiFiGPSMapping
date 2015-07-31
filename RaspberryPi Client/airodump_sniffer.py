import subprocess
import signal
import time

from wifi import Cell, Scheme

home_bssid = 'BC:EE:7B:E8:02:76'
home_essid = 'JX-Test-Network'
home_password = 'P@ssw0rd123'
is_at_home = False

bssid_history = []


def kill_processes():
	
	subprocess.call(["killall", "dhclient"])
	subprocess.call(["killall", "NetworkManager"])
	subprocess.call(["killall", "wpa_supplicant"])

def start_mon(iface):
	
	kill_processes()
	
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
				
		except:
			pass #Ignore error.
		
		if line.find("\x1b[1;1H") >= 0:
			data_list = []
	return data_list

def generate_conf(ssid, password):
	
	config_file = open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w')
	
	config = subprocess.Popen(['wpa_passphrase', ssid, password], stdout = subprocess.PIPE)

	for line in config.stdout:
		config_file.write(line)
		
	print "Generating Configuration File."
	
def connect_home(iface):
	
	wpa_connect = subprocess.Popen(['wpa_supplicant', '-B','-Dwext','-i'+iface,'-c/etc/wpa_supplicant/wpa_supplicant.conf'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	
	print "Connecting to Home Network."
	
def get_ip_addr(iface):
	subprocess.call(['dhclient', iface])
	print "Getting IP Address."
	
def test_con(iface):
	des = "192.168.1.1"
	n = '4'
	ping_test = subprocess.Popen(['ping', des, '-I', iface, '-c', n], stdout = subprocess.PIPE)
	
	for line in ping_test.stdout:
		pass

def get_gateway(iface):
	
	return gateway
		
try:	
	mon_iface = get_mon_iface()
	
	while True:

		cell_table = start_sniff(mon_iface, 5)
		for line in cell_table:
			if line[0] not in bssid_history: #Check if BSSID already detected.
				print 'Found', line[0]
				bssid_history.append(line[0])
			
			if (line[0] == home_bssid): #Check if home network found.
				is_at_home = True
				
		if is_at_home:
			print "Home Network Found."
			generate_conf(home_essid, home_password)
			stop_mon(mon_iface)
			connect_home(mon_iface)
			get_ip_addr(mon_iface)
			test_con(mon_iface)
			break
			
	#FTP/TCP Sending code here:
			
except(KeyboardInterrupt):
	print "\nCtrl-C Detected! Exiting..."