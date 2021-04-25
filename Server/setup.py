import cx_Freeze
import sys
import os

# Include TK Libs
os.environ['TCL_LIBRARY'] = r'C:\\Users\\Utilisateur\\AppData\\Local\\Programs\\Python\\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\Utilisateur\\AppData\\Local\\Programs\\Python\\Python36\tcl\tk8.6'

executables = [
    cx_Freeze.Executable(
        script="yourClientFile.pyw", # .pyw is optional
        base = "Win32GUI"
    )
]

cx_Freeze.setup(
    name='myName',
    options={'build_exe':{'packages':['pygame'], 'include_files':['yourGameDataDirectoryHere']}},
    executables = executables,
    version = '1.0.0'
)