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
BROADCAST_ENABLE=1
AIRPORT_CONTAINER='timemachine'
REBOOT=1

Airport_Mount_Attempt=0
Airport_Mount_Success=0

def millis():
  return int(round(time.time() * 1000))



previous=millis()

def broadcast_mesg(msg):
    print(msg)
    if BROADCAST_ENABLE==1:
        os.system(msg)
    else:
        print ("\nBroadcast Disabled")



mp ='/mnt/Media'
sp='/mnt/Airport'


if os.path.ismount(mp):
    broadcast_mesg('echo "{}mounted" | wall'.format(mp))
    # print('{0} is mounted'.format(mp))
    # cmd='echo "{}mounted" | wall'.format(mp)
    # print(cmd)
    # os.system(cmd)
    if os.path.ismount(sp):
        broadcast_mesg('echo "{}mounted" | wall'.format(sp))
        Airport_Mount_Success=1
        # cmd='echo "{}mounted" | wall'.format(sp)
        # print(cmd)
        # os.system(cmd)
        os.system('docker start {}'.format(AIRPORT_CONTAINER))
    else:
        broadcast_mesg('echo "{} not mounted" | wall'.format(sp))
        
        while (not (os.path.ismount(sp))):
            time.sleep(10)
            os.system('sudo mount -a')
            Airport_Mount_Attempt+=1
            if Airport_Mount_Attempt>10:
                broadcast_mesg('Airport failed \n shutting down airport')
                print ('docker stop {}'.format(AIRPORT_CONTAINER))
                os.system('docker stop {}'.format(AIRPORT_CONTAINER))
                Airport_Mount_Success=0
                break
        if os.path.ismount(sp):
            broadcast_mesg('echo "{}mounted" | wall'.format(sp))
            os.system('docker resstart {}'.format(AIRPORT_CONTAINER))
            

else:
    print('{0} is NOT mounted'.format(mp))
    while True:
        current=millis()
        
        differ=current - previous
       
        time.sleep(10)
        # print('reboooting')
        # os.system('echo "Ext mount has failed will Reboot in a few minitues"| wall')
        if REBOOT==1:
            broadcast_mesg('echo "Ext mount has failed will Reboot in a few minitues"| wall')
        if differ >= INTERVAL:
            previous=millis()
            # print('rebooting now')
            # os.system('echo "Rebooting....."| wall')
            if REBOOT==1:
                broadcast_mesg('echo "Rebooting....."| wall')
                os.system('sudo reboot')
    
    
    
    