from arduino_controller.basicboard.board import ArduinoBasicBoard
from arduino_controller.basicboard.arduino_data import ArduinoData
from arduino_controller.arduino_variable import arduio_variable


class RgbLed(ArduinoBasicBoard):
    FIRMWARE = 15633540938822172
    red = arduio_variable(name="red", type="uint8_t")
    green = arduio_variable(name="green", type="uint8_t")
    blue = arduio_variable(name="blue", type="uint8_t")

    def __init__(self):
        super().__init__()
        self.inocreator.add_creator(RgbLedArduinoData)


class RgbLedArduinoData(ArduinoData):

    def definitions(self):  # name:value
        return {"LED_PIN_RED":3,"LED_PIN_GREEN":5,"LED_PIN_BLUE":6}

    def global_vars(self):  # name:[type,defaultvalue]  array possible: "array[ARRAYSIZE]": ["uint8_t", None]
        return {}

    def includes(self):  # ["<Package.h"]
        return []

    def functions(self):  # name:[returntype,[(argtype,argname),...], stringcode] 
        return {}

    def setup(self):  # stringcode
        return "pinMode(LED_PIN_RED, OUTPUT);pinMode(LED_PIN_GREEN, OUTPUT);pinMode(LED_PIN_BLUE, OUTPUT);"

    def loop(self):  # stringcode
        return "analogWrite(LED_PIN_RED, red);analogWrite(LED_PIN_GREEN, green);analogWrite(LED_PIN_BLUE, blue);"

    def dataloop(self):  # stringcode
        return #'write_data(red,'+str(self.board_instance.get_portcommand_by_name("get_red").byteid)+');'\
               #+'write_data(green,'+str(self.board_instance.get_portcommand_by_name("get_green").byteid)+');'\
               #+'write_data(blue,'+str(self.board_instance.get_portcommand_by_name("get_blue").byteid)+');'


if __name__ == '__main__':
    ins = RgbLed()
    ins.create_ino()
