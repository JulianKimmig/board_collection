from arduino_board_collection.boards.sensor_boards.light_sensors.tsl2591.board import Tsl2591
from arduino_board_collection.boards.signal_boards.light.led.rgb_led.board import RgbLed
from arduino_controller.basicboard.arduino_data import ArduinoData
from arduino_controller.arduino_variable import arduio_variable


class Tsl2591LedAbsorbance(RgbLed,Tsl2591):
    FIRMWARE = 1563437279774598

    def __init__(self):
        super().__init__()
        self.inocreator.add_creator(Tsl2591LedAbsorbanceArduinoData)


class Tsl2591LedAbsorbanceArduinoData(ArduinoData):

    def definitions(self):  # name:value
        return {}

    def global_vars(self):  # name:[type,defaultvalue]  array possible: "array[ARRAYSIZE]": ["uint8_t", None]
        return {}

    def includes(self):  # ["<Package.h"]
        return []

    def functions(self):  # name:[returntype,[(argtype,argname),...], stringcode] 
        return {}

    def setup(self):  # stringcode
        return ""

    def loop(self):  # stringcode
        return ""

    def dataloop(self):  # stringcode
        return ""


if __name__ == '__main__':
    ins = Tsl2591LedAbsorbance()
    ins.create_ino()
