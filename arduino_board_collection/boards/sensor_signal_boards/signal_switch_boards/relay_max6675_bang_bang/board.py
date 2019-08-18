import time

from ArduinoCodeCreator.arduino_data_types import *
from arduino_board_collection.boards.sensor_boards.thermal.max6675.board import Max6675BoardModule
from arduino_board_collection.boards.signal_boards.pulses.dutycycle_digital.board import DutyCycleBoardModule
from arduino_controller.arduino_variable import arduio_variable
from arduino_controller.basicboard.board import ArduinoBoard, ArduinoBoardModule
from arduino_controller.python_variable import python_variable

try:
    _current_time = time.monotonic
except AttributeError:
    _current_time = time.time


class PidBoardModule(ArduinoBoardModule):
    target=0
    current=0
    minimum=0
    maximim=0
    kp = arduio_variable("kp", arduino_data_type=float_,eeprom=True,html_attributes={"step":0.1},minimum=0)
    ki = arduio_variable("ki", arduino_data_type=float_,eeprom=True,html_attributes={"step":0.1},minimum=0)
    kd = arduio_variable("kd", arduino_data_type=float_,eeprom=True,html_attributes={"step":0.1},minimum=0)

    def post_initalization(self):
        self._last_time = _current_time()
        self._last_input = None
        self._integral = 0

    def reset(self):
        self._last_time = None
        self._last_input = None
        self._integral = 0

    def crop(self,value):
        return min(self.maximum,max(self.minimum,value))

    def pid(self):
        if self._last_input is None:
            self._last_time = _current_time()
            time.sleep(0.01)
        now = _current_time()
        if now - self._last_time:
            dt = now - self._last_time
        else:
            return None
        error = self.target - self.current
        d_input = self.current - (self._last_input if self._last_input is not None else self.current)

        # compute integral and derivative terms
        proportional = self.kp*error
        self._integral += self.ki * error * dt
        self._integral = self.crop(self._integral)  # avoid integral windup

        derivative = -self.kd * d_input / dt

        # compute final output
        output = proportional + self._integral + derivative
        output = self.crop(output)

        self._last_input = self.current
        self._last_time = now
        if output is None:
            if self.minimum is None:
                return 0
            return self.minimum
        return output


class RelayMax6675BangBangModule(ArduinoBoardModule):
    max6675 = Max6675BoardModule
    relay = DutyCycleBoardModule
    pid = PidBoardModule

    target_temperature = python_variable("target_temperature", type=np.float,default = 298.15)
    max_temperature = python_variable("max_temperature", type=np.float,default = 300,minimum=0)
    min_temperature = python_variable("min_temperature", type=np.float)

    running = python_variable("running", type=np.bool,default = False,save=False)


    def post_initalization(self):
        self.max6675.temperature.data_point_modification(self.bang_bang_temperature)
        self.relay.duty_cycle.is_data_point = True
        self.relay.duty_cycle.changeable = False
        self.pid.minimum = self.relay.duty_cycle.minimum
        self.pid.maximum = self.relay.duty_cycle.maximum


    def bang_bang_temperature(self,data):
        self.pid.current = data
        self.pid.target  = self.target_temperature
        if self.running:
            pid=self.pid.pid()
            if pid is None:
                pid = 0
            self.relay.duty_cycle=pid
        else:
            self.pid.reset()
            self.relay.duty_cycle = 0
        return data


class RelayMax6675BangBangBoard(ArduinoBoard):
    FIRMWARE = 15657144496468016
    modules = [RelayMax6675BangBangModule]

if __name__ == '__main__':
    ins = RelayMax6675BangBangBoard()
    ins.create_ino()
