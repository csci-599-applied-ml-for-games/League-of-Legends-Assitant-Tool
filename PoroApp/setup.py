__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/3/2020 1:00 PM'

from cx_Freeze import setup, Executable
import sys

base = 'WIN32GUI' if sys.platform == "win32" else None

executables = [Executable("app.py", base=base, icon='resources/ico/poro.ico')]

packages = []
include_files = ['resources/', 'conf/', 'model/', 'utils/']
options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files
    },

}

setup(
    name="poro-app",
    options=options,
    version="1.0",
    description='lol assistant',
    executables=executables
)
