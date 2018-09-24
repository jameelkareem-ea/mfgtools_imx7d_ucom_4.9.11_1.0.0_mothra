#/sys/kernel/debug/gpio: gpio-504 (PCIE_SLOT_MUX_CTRL  )


import sys
import os
import time
import struct

def usage():
	print ""
	print "Usage:"
	print "   ", sys.argv[0], "<num or name> [1|0]"
	print " or"
	print "   ", sys.argv[0], "--list"
	print
	exit(-1)

def list_gpio():
	found = False
	with open("/sys/kernel/debug/gpio", "r") as f:
		for line in f:
			try:
				if found and not line.startswith(" gpio-"):
					found = False
				elif not found and line.find("tca6416")>0:
					found = True
				if found:
					print line.rstrip()
			except:
				# just keep trying
				pass

def get_gpio(arg):
	try:
		return int(arg)
	except ValueError as v:
		# user passed a gpio name
		pass
	with open("/sys/kernel/debug/gpio", "r") as f:
		for line in f:
			try:
				if line.find(arg)>0:
					# " gpio-508 (PCIE_PERST_L        )"
					return int(line.strip().split(" ")[0].split("-")[1])
			except:
				# just keep trying
				pass
	usage()

def export_as_output(gpio):
	dirfile = "/sys/class/gpio/gpio%d/direction" % (gpio)
	if not os.path.exists(dirfile):
		with open("/sys/class/gpio/export", "w") as f:
			f.write("%d" % (gpio))
		time.sleep(1)

	with open(dirfile, "r") as f:
		for line in f:
			if line.strip() == "out":
				return
	with open(dirfile, 'r+') as f:
		f.write(struct.pack('ccc', 'o', 'u', 't'))
	
def set_gpio_value(gpio, value):
	export_as_output(gpio)
	valfile = "/sys/class/gpio/gpio%d/value" % (gpio)
	with open(valfile, 'r+') as f:
		if value == 0:
			f.write(struct.pack('c', '0'))
		else:
			f.write(struct.pack('c', '1'))

if len(sys.argv)==2 and (sys.argv[1]=='--list' or sys.argv[1]=='-l'):
	list_gpio()
	exit(0)
if len(sys.argv) != 3:
	usage()
if sys.argv[2] != "0" and sys.argv[2] != "1":
	usage()
wanted_val = int(sys.argv[2])
wanted_gpio = get_gpio(sys.argv[1])
set_gpio_value(wanted_gpio, wanted_val)
