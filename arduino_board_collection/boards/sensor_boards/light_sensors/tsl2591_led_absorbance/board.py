from arduino_board_collection.boards.sensor_boards.light_sensors.tsl2591.board import Tsl2591
from arduino_board_collection.boards.signal_boards.light.led.rgb_led.board import RgbLed
from arduino_controller.arduino_variable import arduio_variable


class Tsl2591LedAbsorbance(RgbLed,Tsl2591):
    FIRMWARE = 1563437279774598

    def __init__(self):
        super().__init__()
        #self.inocreator.add_creator(Tsl2591LedAbsorbanceArduinoData)



if __name__ == '__main__':
    ins = Tsl2591LedAbsorbance()
    ins.create_ino()
