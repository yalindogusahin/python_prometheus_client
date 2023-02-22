import subprocess as sp

# Print the return code (status=0 mean ping success)
status = sp.call(['tcping', '-c', '1', '-t', '1', 'github.com'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
print(status)

# OR print the full message
status = sp.run(['tcping', '-c', '1', '-t', '1', 'github.com'], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
print(status)