# Description:  This controller gives to its robot the following behavior:
#               According to the messages it receives, the robot change its
#               behavior.
from controller import DifferentialWheels,Camera,DistanceSensor,Emitter
import sys, struct, json


class LidarController (DifferentialWheels):
  timeStep = 64
  resolution = 360
  lidarValues = []

  def initialization(self):
    self.camera = self.getCamera('TiM561')
    self.camera.enable(2*self.timeStep)

    self.emitter = self.getEmitter('emitter')
  
  def run(self) :
    while True :
      lidarValues = self.camera.getRangeImage();

      message = json.dumps(lidarValues)
      
      self.emitter.send(message)
      
      # perform a simulation step, leave the loop when
      # the controller has been killed
      if self.step(self.timeStep) == -1: break

controller = LidarController()
controller.initialization()
controller.run()
