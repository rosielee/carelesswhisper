import os, time, datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import serial
import subprocess

print("Opening serial port to robot arm")
ser = serial.Serial( port='/dev/tty.usbserial',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=5,writeTimeout = 5,rtscts=False,dsrdtr=False)


screen1Path = "Screen1"
screen2Path = "Screen2"
screen3Path = "Screen3"
screen4Path = "Screen4"

screen1Connection = "pi@10.0.0.241"
screen2Connection = "pi@10.0.0.242"
screen3Connection = "pi@10.0.0.243"
screen4Connection = "pi@10.0.0.244"

neutralPosition=b'#0 P1050 #1 P1620 #2 P1430 #3 P1470 #4 P1635 T3000\r\n'
screen1Position=b'#0 P1020 #1 P1670 #2 P1390 #3 P1290 #4 P1855 T3000\r\n'
screen2Position=b'#0 P1790 #1 P1670 #2 P1390 #3 P1290 #4 P975 T3000\r\n'
screen3Position=b'#0 P1020 #1 P1440 #2 P1810 #3 P2040 #4 P1895 T3000\r\n'
screen4Position=b'#0 P1650 #1 P1460 #2 P1810 #3 P2030 #4 P1275 T3000\r\n'
sleepPosition=b'#0 P1380 #1 P2250 #2 P2150 #3 P1520 #4 P1725 T3000\r\n'

remote_path = "~/Desktop/RosieLee/Whispers/Image.jpg"

photoNumber = 0
expTimestamp = "00000000"

def is_image(filename):
    """ File is image if it has a common suffix and it is a regular file """

    if not os.path.isfile(filename):
        return False

    for suffix in ['.jpg', '.png', '.bmp', '.jpeg']:
        if filename.lower().endswith(suffix):
            return True

    return False

class EventHandler(FileSystemEventHandler):

    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)
        self.moveRobot(neutralPosition)

    def on_modified(self, event):
        if(not event.is_directory and is_image(event.src_path)) :
            self.copyFileToScreen(event.src_path)

    def on_created(self, event):
        if(not event.is_directory and is_image(event.src_path)) :
            self.copyFileToScreen(event.src_path)

    def copyFileToScreen(self, filepath):

        print("Found file:"+filepath)
        if(screen1Path in filepath):
            self.moveRobot(screen1Position)
            self.copyFile(screen1Connection,filepath)
            self.takePhoto()
        if(screen2Path in filepath):
            self.moveRobot(screen2Position)
            self.copyFile(screen2Connection,filepath)
            self.takePhoto()
        if(screen3Path in filepath):
            self.moveRobot(screen3Position)
            self.copyFile(screen3Connection,filepath)
            self.takePhoto()
        if(screen4Path in filepath):
            self.moveRobot(screen4Position)
            self.copyFile(screen4Connection,filepath)
            self.takePhoto()

    def copyFile(self, hostname, filepath):

        print('about to copy file')
        command = "scp "+filepath+" "+ hostname+":"+remote_path
        print(command)
        os.system(command)

    def moveRobot(self, position):

        print('about to move robot')
        print(position)
        ser.write(position)
        time.sleep(5)

    def takePhoto(self):
        global photoNumber, expTimestamp
        photoNumber += 1
        destScreen = photoNumber%4 + 1

        # destinationFile = "./Screen{}/photo{}.jpg"
        # destinationFile = destinationFile.format(destScreen,photoNumber)
        destinationFile = "./{}-{}-{}.jpg"
        destinationFile = destinationFile.format(photoNumber, destScreen, expTimestamp)
        command = '/usr/local/Cellar/imagesnap/0.2.5/bin/imagesnap -d "Microsoft® LifeCam HD-6000 for Notebooks" {}'
        command = command.format(destinationFile)

        print('about to takePhoto')

        print(command)
        output = subprocess.check_output(command, shell=True)
        print(output)

if __name__ == '__main__':

    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    _quit = False
    while not _quit:
        continue

    ser.write(sleepPosition)
    ser.close()

    os._exit(0)
