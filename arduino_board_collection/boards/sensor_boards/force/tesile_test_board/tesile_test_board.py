from arduino_board_collection.boards.controller_boards.motors.AccelStepperBoard.board import AccelStepperBoardModule
from arduino_board_collection.boards.sensor_boards.basic.hx711_board.board import HX711Module
from arduino_controller.basicboard.board import ArduinoBoard


class TensileTestBoard(ArduinoBoard):
    FIRMWARE = 17667236029856103160
    modules = [AccelStepperBoardModule,HX711Module]

if __name__ == "__main__":
    ins = TensileTestBoard()
    ins.create_ino()
