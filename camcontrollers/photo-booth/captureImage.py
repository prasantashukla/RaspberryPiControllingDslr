from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# Kill the gphoto process that starts
# whenever we turn on the camera or
# reboot the raspberry pi

def killGphoto2Process():
    p = subprocess.Popen(['pkill', '-INT', 'gphoto2'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    sleep(0.1)
    #p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    #out, err = p.communicate()

    # Search for the process we want to kill
    #for line in out.splitlines():
        #if b'gvfsd-gphoto2' in line:
            # Kill that process!
            #pid = int(line.split(None,1)[0])
            #os.kill(pid, signal.SIGKILL)

#picID = "PiShots"

clearCommand = ["--folder", "/store_00010001/DCIM/100D3200", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

def createSaveFolder(shot_date):
    folder_name = shot_date + picID
    save_location = "/tmp/" + folder_name
    try:
        os.makedirs(save_location)
    except:
        print("Did not create directory.")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(5)
    gp(downloadCommand)
    gp(clearCommand)

def renameFiles(picId):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (picId + ".JPG"))
                print("Renamed the JPG")

#killGphoto2Process()
#gp(clearCommand)


#while True:
#	shot_date = datetime.now().strftime("%Y-%m-%d")
#	shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#	createSaveFolder(shot_date)
#	captureImages()
#	renameFiles()

#>