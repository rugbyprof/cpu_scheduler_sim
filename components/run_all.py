import os, sys

files = []
for filename in os.listdir("."):
    if filename[0] not in ['.','_'] and filename[-1] not in ['c']:
        files.append(filename)

try:
    del files[files.index('run_all.py')]
except:
    print("run_all.py not in list")

try:
    del files[files.index('docs')]
except:
    print("docs not in list")

try:
    del files[files.index('hold.__init__.py')]
except:
    print("hold.__init__.py not in list")

try:
    del files[files.index('sim_components.py')]
except:
    print("sim_components.py not in list")

print(files)

for f in files:
    x = input("Running %s" % f)
    os.system('python3 '+str(f))