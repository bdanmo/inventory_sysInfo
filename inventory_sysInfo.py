import os
import subprocess
from pathlib import Path


def format_size(size):
	for unit in ['B','kB','MB','GB','TB','PB']:
		if size < 1024.0:
			return F"{round(size, 1)}{unit}"
		size /= 1024.0


d1 = subprocess.check_output("wmic bios get serialnumber", shell=True).decode("utf-8")
d2 = subprocess.check_output("wmic csproduct get name & hostname", shell=True).decode("utf-8")
d3 = subprocess.check_output("wmic computersystem get installedphysicalmemory", shell=True).decode("utf-8")
d4 = subprocess.check_output("wmic diskdrive get size", shell=True).decode("utf-8")

SerialNumber = d1.replace("\r", "").strip().split('\n')[-1]
Name = d2.replace("\r", "").strip().split('\n')[1].strip()
Hostname = d2.replace("\r", "").strip().split('\n')[3]
TotalPhysicalMemory = d3.replace("\r", "").strip().split('\n')[-1]
Size = d4.replace("\r", "").strip().split('\n')[-1]

buffer = [
	F"User:                {os.getlogin()}",
	F"SerialNumber:        {SerialNumber}",
	F"Name:                {Name}",
	F"Hostname:            {Hostname}",
	F"TotalPhysicalMemory: {format_size(int(TotalPhysicalMemory))}",
	F"Size:                {format_size(int(Size))}",
]

Path.cwd().joinpath(F"{os.getlogin()}_results.txt").write_text("\n".join(buffer))