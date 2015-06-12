import os, time, datetime
import serial
import subprocess

print("Opening serial port to robot arm")
ser = serial.Serial( port='/dev/tty.usbserial',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=5,writeTimeout = 5,rtscts=False,dsrdtr=False)

screen1Connection = "pi@192.168.1.241"
screen2Connection = "pi@192.168.1.242"
screen3Connection = "pi@192.168.1.243"
screen4Connection = "pi@192.168.1.244"

sleepPosition=b'#0 P1500 #1 P2250 #2 P2150 #3 P1520 #4 P1725 T3000\r\n'

def runCommand(conn):
    command = "ssh {} 'sudo /sbin/shutdown -hP now'"
    command = command.format(conn)
    print(command)
    output = subprocess.check_output(command, shell=True)
    print(output)

if __name__ == '__main__':

    print("Put robot to sleep")        
    ser.write(sleepPosition)
    ser.close()

    runCommand(screen1Connection)
    runCommand(screen2Connection)
    runCommand(screen3Connection)
    runCommand(screen4Connection)

    

    os._exit(0)
