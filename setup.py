import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = 'Console'

setup(
    name="XMLtoCSV",
    version="1.0",
	options = {"build_exe": {"packages":["os"]}},
    description="XML to CSV converter with batch support",
    executables=[Executable("xml_to_csv.py", base=base)]
)