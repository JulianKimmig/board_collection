from ArduinoCodeCreator.arduino_data_types import uint8_t
from arduino_controller.basicboard.board import ArduinoBasicBoard
from arduino_controller.arduino_variable import arduio_variable


class RgbLed(ArduinoBasicBoard):
    FIRMWARE = 15633540938822172

    LED_PIN_RED = 3
    LED_PIN_GREEN = 5
    LED_PIN_BLUE = 6


    red = arduio_variable(name="red", arduino_data_type=uint8_t)
    green = arduio_variable(name="green", arduino_data_type=uint8_t)
    blue = arduio_variable(name="blue", arduino_data_type=uint8_t)

    def __init__(self):
        super().__init__()
        #self.inocreator.add_creator(RgbLedArduinoData)

#
# class RgbLedArduinoData(ArduinoData):
#
#     def __init__(self, board_instance):
#         super().__init__(board_instance)
#         self.setup_func= ArduinoSetupFunction(
#             ArduinoDataFunction.pin_mode(
#                 board_instance.LED_PIN_RED,
#                 ArduinoDataFunction.PIN_MODE_OUT
#             )+
#             ArduinoDataFunction.pin_mode(
#                 board_instance.LED_PIN_GREEN,
#                 ArduinoDataFunction.PIN_MODE_OUT
#             )+
#             ArduinoDataFunction.pin_mode(
#                 board_instance.LED_PIN_BLUE,
#                 ArduinoDataFunction.PIN_MODE_OUT
#             )
#         )
#
#         self.loop_func=ArduinoLoopFunction(
#             ArduinoDataFunction.analog_write(
#                 board_instance.LED_PIN_RED,
#                 board_instance.get_module_var_by_name("red").name
#             )+
#             ArduinoDataFunction.analog_write(
#                 board_instance.LED_PIN_GREEN,
#                 board_instance.get_module_var_by_name("green").name
#             )+
#             ArduinoDataFunction.analog_write(
#                 board_instance.LED_PIN_BLUE,
#                 board_instance.get_module_var_by_name("blue").name
#             )
#         )

if __name__ == '__main__':
    ins = RgbLed()
    ins.create_ino()
