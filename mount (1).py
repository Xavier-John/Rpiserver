# /etc/init.d/mount.py
### BEGIN INIT INFO
# Provides:          mount(1).py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO


import os

import time

INTERVAL = 120000

def millis():
  return int(round(time.time() * 1000))



previous=millis()



mp ='/mnt/Media'
if os.path.ismount(mp):
    print('{0} is mounted'.format(mp))
    cmd='echo "{}mounted" | wall'.format(mp)
    print(cmd)
    os.system(cmd)
else:
    print('{0} is NOT mounted'.format(mp))
    while True:
        current=millis()
        
        differ=current - previous
       
        time.sleep(10)
        print('reboooting')
        os.system('echo "Ext mount has failed will Reboot in a few minitues"| wall')
        if differ >= INTERVAL:
            previous=millis()
            print('rebooting now')
            os.system('echo "Rebooting....."| wall')
            os.system('sudo reboot')
    
    
    
    