from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('src/app11.py', base=base, target_name = 'Termo')
]

setup(name='Termo',
      version = '1.0',
      description = 'Parece completo',
      options = {'build_exe': build_options},
      executables = executables)
