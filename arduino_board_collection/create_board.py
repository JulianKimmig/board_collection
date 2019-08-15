import os
import time

import numpy as np


def generate_pseudorandom_firmware():
    aa = np.uint64(int(str(time.time()).replace(".", ""))).tobytes()
    ba = bytearray(reversed(np.uint64(int(str(time.time()).replace(".", ""))).tobytes()))
    r = np.random.bytes(8)
    for i in range(len(ba)):
        if ba[i] == 0:
            ba[i] = r[i]
        else:
            break
    return np.frombuffer(ba,dtype=np.uint64)

def create_board(path, name, superboard="ArduinoBasicBoard"):
    camelcase = "".join(x for x in name.title() if not x.isspace())
    snakename = name.lower().replace(" ", "_")
    os.makedirs(os.path.join(path, snakename), exist_ok=True)
    if os.path.exists(os.path.join(path, snakename, "board.py")):
        raise ValueError(
            name + "already exists as board: " + str(os.path.join(path, snakename))
        )

    with open(os.path.join(path, snakename, "board.py"), "w+") as f:
        code = ""
        if superboard == "ArduinoBasicBoard":
            code += (
                "from arduino_controller.basicboard.board import ArduinoBasicBoard\n"
            )
        code += "from ArduinoCodeCreator.arduino_data_types import *"
        code += "from arduino_controller.arduino_variable import arduio_variable\n"

        # boardclass
        code += "\n\nclass " + camelcase + "(" + superboard + "):\n"
        code += "\tFIRMWARE = " + str(generate_pseudorandom_firmware()) + "\n"

        # end
        code += "\n\nif __name__ == '__main__':\n"
        code += "\tins = " + camelcase + "()\n"
        code += "\tins.create_ino()\n"
        f.write(code.replace("\t", "    "))


if __name__ == "__main__":
    create_board(
        path=os.path.join(os.path.dirname(__file__), "boards", "test"),
        name="Testboard " + str(int(time.time())),
    )
