import os
import subprocess
from pathlib import Path

def format_size(size, device):
	for unit in ['B','kB','MB','GB','TB','PB']:
		if size < 1024:
			size_int = round(size, 0)
			if device == "RAM":
				while size_int % 4 != 0:
					size_int += 1
			elif device == "HD":
				while size_int % 8 != 0 and size_int % 10 != 0:
					size_int += 1
			return F"{int(size_int)}{unit}"
		size /= 1024


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
	F"TotalPhysicalMemory: {format_size(int(TotalPhysicalMemory), 'RAM')}",
	F"Size:                {format_size(int(Size), 'HD')}",
	F"Hostname:            {Hostname}",
	F"User:                {os.getlogin()}"
]

Path.cwd().joinpath(F"{SerialNumber}_results.txt").write_text("\n".join(buffer))