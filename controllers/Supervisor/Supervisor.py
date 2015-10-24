from controller import Supervisor,Receiver,Camera,Display,Node,Field
import sys
import struct
import socket
import json
import numpy




class Supervisor (Supervisor) :
  timeStep = 64
  resolution = 360
  movementFactor = 1
  
  def initialization(self):
    self.receiver = self.getReceiver('receiver')
    self.receiver.enable(self.timeStep)

    self.myBot = self.getFromDef('MYLIDAR')
    self.mySick = self.getFromDef('SICK')

    if self.myBot is None:
      # robot might be None if the controller is about to quit
      sys.exit(1);

    self.keyboardEnable(self.timeStep)

    self.translationField = self.myBot.getField('translation')
    self.rotationField = self.myBot.getField('rotation')
    self.resolutionField = self.mySick.getField('resolution')

    # initialise the UDP connection
    self.HOST, self.PORT = "localhost", 9999
    # SOCK_DGRAM is the socket type to use for UDP sockets
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


  def run(self):
    
    
    #main loop
    while True:
      if self.receiver.getQueueLength()>0 :

        message = self.receiver.getData()
        self.receiver.nextPacket()
        
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 64000)
        self.sock.sendto(message + "\n", (self.HOST, self.PORT))        
        received = self.sock.recv(1024)
        
      # process keyboard event to move the LIDAR 
      k = self.keyboardGetKey()
      message = ''
      if k==ord('X'):
        if self.movementFactor != 10:
          print 'large movement step'
          self.movementFactor = 10
        else:
          print 'small movement step'
          self.movementFactor = 1
      if k==ord('A'):
        print 'translate left'
        translationValues = numpy.array(self.translationField.getSFVec3f())
        translationStep = numpy.array([0., 0., 0.005*self.movementFactor])
        self.translationField.setSFVec3f((translationValues + translationStep).tolist());
      elif k==ord('D'):
        print 'translate right'
        translationValues = numpy.array(self.translationField.getSFVec3f())
        translationStep = numpy.array([0., 0., -0.005*self.movementFactor])
        self.translationField.setSFVec3f((translationValues + translationStep).tolist());
      elif k==ord('W'):
        print 'translate front'
        translationValues = numpy.array(self.translationField.getSFVec3f())
        translationStep = numpy.array([-0.005*self.movementFactor, 0., 0.])
        self.translationField.setSFVec3f((translationValues + translationStep).tolist());
      elif k==ord('S'):
        print 'translate rear'
        translationValues = numpy.array(self.translationField.getSFVec3f())
        translationStep = numpy.array([0.005*self.movementFactor, 0., 0.])
        self.translationField.setSFVec3f((translationValues + translationStep).tolist());
      elif k==ord('J'):
        print 'rotate left'
        rotationValues = self.rotationField.getSFRotation()
        rotationStep = numpy.array([0.,0.,0.,0.02*self.movementFactor])
        self.rotationField.setSFRotation((rotationValues + rotationStep).tolist());
      elif k==ord('L'):
        print 'rotate right'
        rotationValues = self.rotationField.getSFRotation()
        rotationStep = numpy.array([0.,0.,0.,-0.02*self.movementFactor])
        self.rotationField.setSFRotation((rotationValues + rotationStep).tolist());
        
      if self.step(self.timeStep) == -1: break
  

controller = Supervisor()
controller.initialization()
controller.run()
