import os
import subprocess
from pathlib import Path


def format_size(size):
	for unit in ['B','kB','MB','GB','TB','PB']:
		if size < 1024.0:
			return F"{round(size, 1)}{unit}"
		size /= 1024.0

def round_RAM(RAM):
	intRAM = int(round(RAM, 0))
	while intRAM % 4 != 0:
		intRAM +=1
	return intRAM

def round_HD(HD):
	intHD = int(round(HD, 0))
	while intHD % 8 != 0 and intHD % 10 != 0:
		intHD += 1
	return intHD


d1 = subprocess.check_output("wmic bios get serialnumber", shell=True).decode("utf-8")
d2 = subprocess.check_output("wmic csproduct get name & hostname", shell=True).decode("utf-8")
d3 = subprocess.check_output("wmic computersystem get totalphysicalmemory", shell=True).decode("utf-8")
d4 = subprocess.check_output("wmic diskdrive get size", shell=True).decode("utf-8")
d5 = subprocess.check_output('systeminfo | find "System Manufacturer"', shell=True).decode("utf-8")

SerialNumber = d1.replace("\r", "").strip().split('\n')[-1]
Model = d2.replace("\r", "").strip().split('\n')[1].strip()
Manufacturer = d5.replace("\r", "").strip().split(':')[-1].strip()
Hostname = d2.replace("\r", "").strip().split('\n')[3]
TotalPhysicalMemory = d3.replace("\r", "").strip().split('\n')[-1]
Size = d4.replace("\r", "").strip().split('\n')[-1]

buffer = [
	F"SerialNumber:        {SerialNumber}",
	F"Make/Model:          {Manufacturer} {Model}",
	F"TotalPhysicalMemory: {format_size(int(TotalPhysicalMemory))}",
	F"Size:                {format_size(int(Size))}"
	F"Hostname:            {Hostname}",
	F"User:                {os.getlogin()}"
]

Path.cwd().joinpath(F"{os.getlogin()}_results.txt").write_text("\n".join(buffer))