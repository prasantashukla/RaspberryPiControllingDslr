from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# Kill the gphoto process that starts
# whenever we turn on the camera or
# reboot the raspberry pi

clearCommand = ["--folder", "/store_00010001/DCIM/100D3200", \
                "--delete-all-files", "-R"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

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

def runGpCommand(cmd):
    gp(cmd)

def createSaveFolder(folder_name):
    save_location = folder_name
    try:
        os.makedirs(save_location)
    except:
        print("Did not create directory.")
    #os.chdir(save_location)
    sleep(0.1)
    return folder_name

def captureImages(folder_name):
    print("killing gphoto2 process")
    killGphoto2Process()
    print("Capturing image")
    gp(triggerCommand)
    sleep(1)
    print("Downloading data")
    os.chdir(folder_name)
    gp(downloadCommand)
    print("Clearing the data from the photo")
    gp(clearCommand)
    return folder_name

def renameFiles(folder_name, picId):
    cwd = os.getcwd()
    #print("insidee renamefiles with current directory as  " + os.getcwd())
    #print(os.listdir(folder_name))

    latestFileCaptured = None
    for filename in os.listdir("."):
        print(filename)
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                picName = picId+".JPG"
                os.rename(filename, picName)
                print("Renamed the JPG as " + picName)
                latestFileCaptured = picName
    return cwd+"/"+latestFileCaptured

#killGphoto2Process()
#gp(clearCommand)


#while True:
#	shot_date = datetime.now().strftime("%Y-%m-%d")
#	shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#	createSaveFolder(shot_date)
#	captureImages()
#	renameFiles()

#>