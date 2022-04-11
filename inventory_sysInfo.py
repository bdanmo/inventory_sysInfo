import os
import subprocess
from pathlib import Path
from datetime import datetime

outputDir = Path("redacted for security")
outputCSV = outputDir.joinpath("output.csv")
now = datetime.now()
nowStr = now.strftime("%d/%m/%Y %H:%M:%S")

def format_size(size, device):
	for unit in ['B','KB','MB','GB','TB','PB']:
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
d5 = subprocess.check_output("wmic computersystem get manufacturer", shell=True).decode("utf-8")

SerialNumber = d1.replace("\r", "").strip().split('\n')[-1]
Model = d2.replace("\r", "").strip().split('\n')[1].strip()
Manufacturer = d5.replace("\r", "").strip().split('\n')[-1].strip()
Hostname = d2.replace("\r", "").strip().split('\n')[3]
Memory = d3.replace("\r", "").strip().split('\n')[-1]
Size = d4.replace("\r", "").strip().split('\n')[-1]

buffer = [
	F"{SerialNumber}",
	F"{Manufacturer} {Model}",
	F"{format_size(int(Memory), 'RAM')}",
	F"{format_size(int(Size), 'HD')}",
	F"{Hostname}",
	F"{os.getlogin()}",
	F"{nowStr}"
]

with open(outputCSV, "a") as f:
    f.write(F"\n{';'.join(buffer)}")
