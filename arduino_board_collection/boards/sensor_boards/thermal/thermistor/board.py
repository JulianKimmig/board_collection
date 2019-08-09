from ArduinoCodeCreator.arduino import Arduino
from ArduinoCodeCreator.arduino_data_types import *
from arduino_board_collection.boards.sensor_boards.basic.analog_read_board.board import AnalogReadModule
from arduino_controller.basicboard.board import ArduinoBoardModule, ArduinoBoard
from arduino_controller.arduino_variable import arduio_variable
from arduino_controller.python_variable import python_variable

class ThermistorBoardModule(ArduinoBoardModule):
    analog_read_module = AnalogReadModule

    #analog_read_module.analog_value.is_data_point = False

    # arduino_variables
    thermistor_base_resistance = arduio_variable(name="thermistor_base_resistance", arduino_data_type=uint32_t, eeprom=True,default=10**5)
    reference_resistance = arduio_variable(name="reference_resistance", arduino_data_type=uint32_t, eeprom=True,default=10**5)

    # python_variables
    temperature = python_variable("temperature", type=np.float, changeable=False, is_data_point=True, save=False)
    reference_temperature = python_variable("reference_temperature", type=np.float,default = 298.15,minimum=0)
    a = python_variable("a", type=np.float,default=1.009249522)
    b = python_variable("b", type=np.float,default=2.378405444)
    c = python_variable("c", type=np.float,default=2.019202697)




    @classmethod
    def module_arduino_code(cls,board,arduino_code_creator):
        arduino_code_creator.setup.add_call(Arduino.analogReference(Arduino.EXTERNAL))


    def post_initalization(self):
        self.analog_read_module.analog_value.setter = self.resistance_to_temperature

    def resistance_to_temperature(self,var, instance, data, send_to_board=True):
        var.default_setter(
            var=var, instance=instance, data=data, send_to_board=send_to_board
        )
        try:
            R2 = self.reference_resistance * (1023.0/data  - 1)
            print(R2)
            logR2 = np.log(R2)
            T = (1.0 / (self.a/10**3 + self.b*logR2/10**4 + self.c*logR2*logR2*logR2/10**7))
            self.temperature = T
        except ZeroDivisionError:
            pass



class ThermistorBoard(ArduinoBoard):
    FIRMWARE = 15650180050147572
    modules = [ThermistorBoardModule]

class DualThermistorBoard(ArduinoBoard):
    FIRMWARE = 15650180050147573
    modules = [ThermistorBoardModule,ThermistorBoardModule]

if __name__ == '__main__':
    ins = DualThermistorBoard()
    ins.create_ino()