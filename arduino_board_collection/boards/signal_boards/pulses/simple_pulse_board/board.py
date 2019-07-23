from arduino_controller.basicboard.board import ArduinoBasicBoard
from arduino_controller.basicboard.arduino_data import ArduinoData
from arduino_controller.arduino_variable import arduio_variable


class SimplePulseBoard(ArduinoBasicBoard):
    FIRMWARE = 15627604053828192
    CLASSNAME = "Simple Pulse Board"
    PULSE_TYPE_SQUARE = 0
    PULSE_TYPE_SIN = 1

    pulse_type = arduio_variable(name="pulse_type", default=1,maximum=1)
    wavelength = arduio_variable(name="wavelength", type="uint16_t",minimum=1,default=1000)  # in millisec
    current_val = arduio_variable(name="current_val", type="uint16_t",is_data_point=True)  # in mV
    running = arduio_variable(name="pulsing", type="bool")

    def __init__(self):
        super().__init__()
        self.inocreator.add_creator(SimplePulseBoardArduinoData)

    def get_frequency(self):
        return 1000 / self.wavelength

    def set_frequency(self, hertz):
        self.wavelength = 1000 / hertz

    frequency = property(get_frequency, set_frequency)


class SimplePulseBoardArduinoData(ArduinoData):

    def definitions(self):  # name:value
        return {'PULSE_TYPE_SQUARE': 0,
                'PULSE_TYPE_SIN': 1,
                'PULSEPIN':6}

    def global_vars(self):  # name:[type,defaultvalue]  array possible: "array[ARRAYSIZE]": ["uint8_t", None]
        return {'pulse_pos': ["double", 0],
                'max_current_val': ["uint16_t", -1]}

    def includes(self):  # ["<Package.h"]
        return []

    def functions(self):  # name:[returntype,[(argtype,argname),...], stringcode]
        return {}

    def setup(self):  # stringcode
        return ""

    def loop(self):  # stringcode
        return "if(pulsing){\n" \
               "pulse_pos = (ct%wavelength)/(1.0*wavelength);\n" \
               "if(pulse_type == PULSE_TYPE_SQUARE){\n" \
               "if(pulse_pos<0.5)\ncurrent_val = max_current_val;\nelse\ncurrent_val = 0;\n" \
               "}else if(pulse_type == PULSE_TYPE_SIN){\n" \
               "current_val = (1+sin(pulse_pos*2*PI))/2*max_current_val;\n"\
               "}\n" \
               "analogWrite(PULSEPIN, map(current_val, 0, max_current_val, 0, 255));\n" \
               "}"

    def dataloop(self):  # stringcode
        return 'write_data(current_val,'+str(self.board_instance.get_portcommand_by_name("get_current_val").byteid)+');'


if __name__ == '__main__':
    ins = SimplePulseBoard()
    ins.create_ino()
