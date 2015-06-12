from tkinter import *
import serial

print("Opening")
ser = serial.Serial( port='/dev/tty.usbserial',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=5,writeTimeout = 5,rtscts=False,dsrdtr=False)



neutralPosition=b'#0 P1380 #1 P1500 #2 P690 #3 P1470 #4 P1725 T3000\r\n'
templatePosition='#0 P{} #1 P{} #2 P{} #3 P{} #4 P{} T{}\r\n'

baseVal=1500
shoulderVal=1500
elbowVal=690
wristVal=1470
cameraVal=1725
speedVal = 100

changeVal=10



class KeyDemo( Frame ):



   def __init__( self ):


      Frame.__init__( self )
      self.pack( expand = YES, fill = BOTH )
      self.master.title( "Calibrate Robot arm" )
      self.master.geometry( "350x350" )

      self.message1 = StringVar()
      self.line1 = Label( self, textvariable = self.message1 )
      self.message1.set( "Q: Base Clockwise\nA: Base Anti-clockwise\nW: Shoulder Up\nS: Shoulder down\nE: Elbow Up\nD: Elbow Down\nR: Wrist Up\nF: Wrist Down\nT: Camera Clockwise\nG: Camera Anti-clockwise" )
      self.line1.pack()

      self.message2 = StringVar()
      self.line2 = Label( self, textvariable = self.message2 )
      self.message2.set( "" )
      self.line2.pack()

      self.master.bind( "<KeyPress>", self.keyPressed )


      self.neutralRobot()

      

   def keyPressed( self, event ):

      global baseVal,shoulderVal,elbowVal,wristVal,cameraVal,changeVal,speedVal
      
      #self.message1.set( "Key pressed: " + event.char )
      if event.char == 'q':
          baseVal+=changeVal
      elif event.char == 'a':
          baseVal-=changeVal
      elif event.char == 'w':
          shoulderVal+=changeVal
      elif event.char == 's':
          shoulderVal-=changeVal
      elif event.char == 'd':
          elbowVal+=changeVal
      elif event.char == 'e':
          elbowVal-=changeVal
      elif event.char == 'r':
          wristVal+=changeVal
      elif event.char == 'f':
          wristVal-=changeVal
      elif event.char == 't':
          cameraVal+=changeVal
      elif event.char == 'g':
          cameraVal-=changeVal
      elif event.char == 'n':
          self.neutralRobot()
          return
      elif event.char == 'p':
          ser.close()
          os._exit(0)
      self.moveRobot()

   def moveRobot(self):
      global baseVal,shoulderVal,elbowVal,wristVal,cameraVal,templatePosition,speedVal
      newPosition = templatePosition.format(baseVal,shoulderVal,elbowVal,wristVal,cameraVal,speedVal)
      
      self.message2.set(newPosition)
      ser.write(bytes(newPosition, 'utf-8'))

   def neutralRobot(self):
      global baseVal,shoulderVal,elbowVal,wristVal,cameraVal,templatePosition,speedVal
      baseVal=1500
      shoulderVal=1500
      elbowVal=690
      wristVal=1470
      cameraVal=1725
      speedVal=3000
      self.moveRobot()
      speedVal=100
   
KeyDemo().mainloop()
