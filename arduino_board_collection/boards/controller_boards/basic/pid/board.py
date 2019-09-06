from ArduinoCodeCreator.arduino import *
from ArduinoCodeCreator.arduino_data_types import *
from ArduinoCodeCreator.basic_types import *
from ArduinoCodeCreator.statements import *
from arduino_controller.arduino_variable import arduio_variable
from arduino_controller.basicboard.board import (
    ArduinoBoardModule,
    BasicBoardModule,
    ArduinoBoard,
)
from arduino_controller.python_variable import python_variable


try:
    _current_time = time.monotonic
except AttributeError:
    _current_time = time.time


class PIDModule(ArduinoBoardModule):
    # depencies
    basic_board_module = BasicBoardModule

    target = 0
    current = 0
    minimum = 0
    maximim = 0

    # python_variables
    kp = python_variable("kp", type=np.float, html_attributes={"step": 0.1}, minimum=0)
    ki = python_variable(
        "ki", type=np.float, html_attributes={"step": 0.001}, minimum=0
    )
    kd = python_variable("kd", type=np.float, html_attributes={"step": 0.01}, minimum=0)

    # arduino_variables

    def post_initalization(self):
        self._last_time = _current_time()
        self._last_input = None
        self._integral = 0

    def instance_arduino_code(self, ad):
        ad.loop.add_call()
        ad.setup.add_call()
        self.basic_board_module.dataloop.add_call()

    def crop(self, value):
        return min(self.maximum, max(self.minimum, value))

    def reset(self):
        self._last_time = None
        self._last_input = None
        self._integral = 0

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
        d_input = self.current - (
            self._last_input if self._last_input is not None else self.current
        )

        # compute integral and derivative terms
        proportional = self.kp * error
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


class PIDBoard(ArduinoBoard):
    FIRMWARE = 12178229842355107743
    modules = [PIDModule]


if __name__ == "__main__":
    ins = PIDBoard()
    ins.create_ino()
