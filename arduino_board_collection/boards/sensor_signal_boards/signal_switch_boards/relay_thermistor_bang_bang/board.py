import time
from functools import partial

from ArduinoCodeCreator.arduino_data_types import *
from arduino_board_collection.boards.sensor_boards.thermal.thermistor.board import ThermistorBoardModule
from arduino_board_collection.boards.signal_boards.pulses.dutycycle_digital.board import DutyCycleBoardModule
from arduino_board_collection.boards.signal_boards.switches.relay.board import RelayBoardModule
from arduino_controller.basicboard.board import ArduinoBoard, ArduinoBoardModule
from arduino_controller.python_variable import python_variable

try:
    _current_time = time.monotonic
except AttributeError:
    _current_time = time.time



class RelayThermistorBangBangModule(ArduinoBoardModule):
    thermistor = ThermistorBoardModule
    relay = DutyCycleBoardModule

    target_temperature = python_variable("target_temperature", type=np.float,default = 298.15)
    max_temperature = python_variable("max_temperature", type=np.float,default = 300,minimum=0)
    min_temperature = python_variable("min_temperature", type=np.float)

    running = python_variable("running", type=np.bool,default = False,save=False)


    def post_initalization(self):
        self.thermistor.temperature.setter = self.bang_bang_temperature
        self._last_time = _current_time()
        self._last_input = None
        self._integral = 0



    def bang_bang_temperature(self,var, instance, data):
        current =var.default_setter(var = var, instance =instance, data = data)
        target  = self.target_temperature
        if self.running:
            if self._last_time is None:
                self._last_time = _current_time()
                time.sleep(0.01)
            now = _current_time()
            dt = now - self._last_time
            error = target - current

        else:
            self.reset()


    def reset(self):
        self._last_time = None
        self._last_input = None
        self._integral = 0

    def pid(self,input,target):
        if self._last_input is None:
            self._last_time = _current_time()
            time.sleep(0.01)
        now = _current_time()
        if now - self._last_time:
            dt = now - self._last_time
        else:
            return None
        error = target - input
        d_input = input - (self._last_input if self._last_input is not None else input)

        # compute integral and derivative terms
        proportional = self.kp*error
        self._integral += self.ki * error * dt
        self._integral = min(self.max_on_time,max(self.min_on_time,self._integral))  # avoid integral windup

        derivative = -self.kd * d_input / dt

        # compute final output
        output = proportional + self._integral + derivative
        output = min(self.max_on_time,max(self.min_on_time,output))

        self._last_input = input
        self._last_time = now
        return output

class Relay2ThermistorBangBangBoard(ArduinoBoard):
    FIRMWARE = 15657144496468015
    modules = [RelayThermistorBangBangModule,ThermistorBoardModule]

if __name__ == '__main__':
    ins = Relay2ThermistorBangBangBoard()
    ins.create_ino()
