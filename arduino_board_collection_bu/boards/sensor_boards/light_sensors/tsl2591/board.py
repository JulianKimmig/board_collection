import struct

import numpy as np
import scipy.interpolate

from ArduinoCodeCreator.arduino_data_types import (
    uint32_t,
    uint8_t,
    boolean,
    uint16_t,
    float_,
)
from ArduinoCodeCreator.basic_types import ArduinoClass, Function, ArduinoEnum
from arduino_controller.arduino_variable import arduio_variable
from arduino_controller.basicboard.board import (
    ArduinoBasicBoard,
    COMMAND_FUNCTION_COMMUNICATION_ARGUMENTS,
    WRITE_DATA_FUNCTION,
)
from arduino_controller.python_variable import python_variable

REL_IR_SENSITIVITY = np.array(
    [
        (301.5282884840381, 0.0003707002656236913),
        (311.14929801103125, 0.00033747854764376584),
        (320.77030753802444, 0.0003042568296638404),
        (330.3913170650176, 0.0002710351116839149),
        (340.0123265920107, 0.00023781339370398946),
        (349.63333611900384, 0.00020459167572384196),
        (359.254345645997, 0.0006843132833542764),
        (368.8753551729901, 0.001420506553790002),
        (378.4963646999833, 0.0013872848358100764),
        (388.11737422697644, 0.001354063117830151),
        (397.7383837539696, 0.0010643697370449345),
        (407.3593932809627, 0.0012876196818703),
        (416.9804028079559, 0.0012543979638903746),
        (426.60141233494903, 0.0012211762459104492),
        (436.22242186194217, 0.0011879545279305237),
        (445.8434313889353, 0.0011547328099505982),
        (455.4644409159285, 0.0011215110919704507),
        (465.0854504429216, 0.0016012326996008852),
        (474.70645996991476, 0.0033633126212573305),
        (484.3274694969079, 0.006664222519745078),
        (494.58987965903395, 0.011459002336731139),
        (503.5694885508942, 0.016160508225522285),
        (513.5111983954538, 0.024430975817301803),
        (522.8115076048805, 0.030639671951514735),
        (532.4325171318736, 0.041634731734158326),
        (542.0535266588668, 0.054040385662230794),
        (551.67453618586, 0.06683074708451109),
        (560.8679452894312, 0.0804062484417174),
        (569.4199537578695, 0.09448265948002144),
        (578.6133628614407, 0.10751672066019469),
        (588.2343723884339, 0.12094826123948788),
        (597.8553819154271, 0.13296920767335263),
        (607.4763914424202, 0.14422073911880162),
        (616.6698005459914, 0.15544525023362699),
        (625.0347338291826, 0.16980727576400867),
        (631.2883900217282, 0.18741810846517937),
        (637.0609957379241, 0.20294676999195693),
        (641.0124817936535, 0.21811533182563037),
        (645.9604295503927, 0.23428038700004528),
        (651.7330352665887, 0.24815266903787248),
        (657.7805269692701, 0.2618408078388966),
        (665.2024486043791, 0.2745013672630695),
        (672.8992562259735, 0.2887410261322251),
        (680.5960638475681, 0.3002938390100879),
        (688.2928714691626, 0.3159379855565101),
        (695.7147931042716, 0.32857564572507536),
        (701.7622848069531, 0.3428744313423022),
        (707.5348905231489, 0.3563192606087875),
        (713.3074962393448, 0.3695503634896018),
        (719.0801019555407, 0.38299519275608707),
        (725.5742833862611, 0.3943536981334316),
        (733.7521414842053, 0.4021799043465579),
        (744.644498698694, 0.41175997997103997),
        (753.3950359351495, 0.418569008369016),
        (763.9781464148421, 0.4275089726774203),
        (772.9577553067023, 0.43512937034766097),
        (781.857189119171, 0.4488198742186079),
        (788.3513705498914, 0.46333084378459966),
        (794.8455519806117, 0.4758648442831346),
        (803.0234100785559, 0.48497340881028717),
        (813.3659953200736, 0.49282419909471864),
        (822.9870048470667, 0.4914231285084443),
        (832.0582424010888, 0.4862013072366246),
        (840.7324224190763, 0.47583106886985505),
        (849.2844308875146, 0.4671812408984757),
        (851.8500334280461, 0.4570417510928755),
        (859.2719550631551, 0.44617103545467096),
        (865.3194467658366, 0.4325021968898066),
        (871.0920524820324, 0.41773514324771943),
        (874.9404562928297, 0.40137178605669566),
        (880.7130620090256, 0.38735277476445706),
        (886.4856677252214, 0.37119649961550827),
        (890.6547718535852, 0.35696929889059525),
        (894.5031756643824, 0.34562851176284015),
        (898.3515794751797, 0.3345014510207559),
        (902.1999832859769, 0.32273321112165876),
        (906.4973675413672, 0.31271597723822486),
        (913.1496084143167, 0.2988801758107126),
        (919.1971001169982, 0.2839900436134426),
        (924.9697058331941, 0.2711465274423944),
        (931.0171975358755, 0.2594317586893793),
        (938.4391191709844, 0.24775040940266535),
        (946.135926792579, 0.23570172283428747),
        (953.8327344141735, 0.22317215189814976),
        (961.529542035768, 0.21048228617275888),
        (969.2263496573626, 0.19667035692259527),
        (976.6482712924715, 0.18398144038914666),
        (982.6957629951529, 0.1698546167121302),
        (988.4683687113488, 0.15572874222705602),
        (994.2409744275448, 0.14096168858496883),
        (1000.0135801437406, 0.12833189879959161),
        (1005.7861858599365, 0.11677074094256934),
        (1011.5587915761324, 0.10478213031420525),
        (1017.6062832788139, 0.092609376449038),
        (1025.0282049139228, 0.08074483311746328),
        (1032.7250125355172, 0.06949762049535158),
        (1040.8494205805337, 0.0570912467633895),
        (1049.4014290489722, 0.05100613542006238),
        (1052.6084322246365, 0.041591100544544846),
        (1060.7633831570402, 0.03786852794556306),
        (1065.7571452448606, 0.029790746318067107),
        (1074.2327964948306, 0.025548016534713502),
        (1084.9991642988466, 0.019465436369898947),
        (1094.2994735082734, 0.01661213375166093),
        (1101.9962811298678, 0.012994953098004247),
    ]
)
REL_FULL_SENSITIVITY = np.array(
    [
        (365.9890523, 0.007842265),
        (377.5342637, 0.007802399),
        (385.2310714, 0.007775821),
        (400.4322664, 0.007723331),
        (412.169898, 0.008537706),
        (423.4745842, 0.013254082),
        (427.5635133, 0.024941483),
        (431.8242461, 0.035826816),
        (434.5731059, 0.047724937),
        (438.1466238, 0.061085763),
        (442.3157279, 0.074688791),
        (443.9192295, 0.086309969),
        (446.8055323, 0.096900831),
        (449.6918352, 0.110141901),
        (454.364897, 0.12624684),
        (456.1058416, 0.138545362),
        (458.7630728, 0.149680491),
        (462.0617046, 0.162492684),
        (463.1612485, 0.174726249),
        (465.7268511, 0.185745672),
        (467.0096523, 0.198564825),
        (468.9338543, 0.210355878),
        (470.8580562, 0.224839882),
        (473.2098585, 0.243425957),
        (475.2562319, 0.260272743),
        (476.6306619, 0.280602536),
        (474.70646, 0.270350314),
        (478.5548638, 0.306243058),
        (478.5548638, 0.29418889),
        (480.4790657, 0.33188358),
        (480.4790657, 0.31957294),
        (482.8843181, 0.35816362),
        (482.4032676, 0.34495699),
        (484.3274695, 0.382431847),
        (483.846419, 0.37162506),
        (486.6792718, 0.409943543),
        (486.2516714, 0.395725091),
        (488.6569238, 0.433161648),
        (486.2516714, 0.424193445),
        (490.5811257, 0.457840401),
        (488.1758733, 0.446414345),
        (492.4518775, 0.485867719),
        (491.0621762, 0.471624092),
        (494.3760794, 0.507091229),
        (490.1000752, 0.498556939),
        (496.1475669, 0.531877373),
        (496.3537314, 0.521617794),
        (498.2244833, 0.556804946),
        (495.8726809, 0.542992094),
        (500.2708567, 0.573814571),
        (502.7142877, 0.595117708),
        (501.6452866, 0.583580174),
        (503.8100138, 0.611357129),
        (506.0434624, 0.626188135),
        (507.9676643, 0.640837014),
        (509.8918662, 0.654020341),
        (511.5411822, 0.66958614),
        (514.015156, 0.683683538),
        (515.7561006, 0.697233886),
        (517.0389019, 0.708770681),
        (519.6045044, 0.7207305),
        (521.5287063, 0.731623901),
        (523.3612796, 0.745021271),
        (527.5151123, 0.759601386),
        (530.5083152, 0.774307639),
        (535.456263, 0.787663719),
        (539.1672238, 0.799100533),
        (543.0156276, 0.80998729),
        (546.8640314, 0.821087773),
        (551.1247642, 0.832492156),
        (554.1485101, 0.845122104),
        (558.3023427, 0.85966151),
        (561.5704317, 0.873674747),
        (565.1439495, 0.887951543),
        (570.4355048, 0.900619458),
        (574.2151871, 0.912101833),
        (579.5754638, 0.922708579),
        (586.3101705, 0.932089284),
        (595.93118, 0.936188106),
        (602.6658867, 0.927544553),
        (606.1019615, 0.915838802),
        (608.7591927, 0.903372431),
        (611.0040949, 0.89267836),
        (615.1731991, 0.879626655),
        (620.7533846, 0.86780969),
        (629.1236629, 0.879578483),
        (631.5289153, 0.895279067),
        (627.6805114, 0.867401063),
        (634.8428185, 0.914253651),
        (630.5668143, 0.903297129),
        (636.9808207, 0.928922147),
        (638.9050226, 0.940243001),
        (640.8292245, 0.952418761),
        (642.7534264, 0.963739615),
        (644.0362276, 0.974806212),
        (650.450234, 0.989383951),
        (660.7126442, 0.990179673),
        (664.0479275, 0.981405374),
        (668.0887515, 0.972201187),
        (676.1062594, 0.962698299),
        (685.8438872, 0.953701119),
        (696.2645651, 0.951616694),
        (699.5631969, 0.945926288),
        (710.4211934, 0.953781405),
        (721.0043039, 0.959088021),
        (725.8148086, 0.95169785),
        (731.5874143, 0.94173964),
        (737.1194948, 0.928576365),
        (740.2463229, 0.916767871),
        (744.0947267, 0.907265131),
        (748.6647063, 0.895355477),
        (752.7536353, 0.884494744),
        (756.4645961, 0.874284128),
        (762.1341196, 0.861807356),
        (766.2230486, 0.850465738),
        (771.0335534, 0.842541251),
        (779.692462, 0.838407805),
        (789.7507901, 0.847955787),
        (800.3776325, 0.851256138),
        (806.7687316, 0.842417856),
        (814.1906533, 0.830484615),
        (815.6750376, 0.821099954),
        (819.963259, 0.812145277),
        (825.6327825, 0.799874599),
        (828.7596106, 0.7882264),
        (832.9287147, 0.777354703),
        (835.0819883, 0.765561785),
        (838.8616706, 0.752702251),
        (843.0536819, 0.738787927),
        (844.5380662, 0.728414019),
        (848.0016296, 0.717672994),
        (849.9258315, 0.706595323),
        (853.2931849, 0.694946294),
        (855.6984372, 0.682723526),
        (858.5847401, 0.671899004),
        (860.8296423, 0.66077748),
        (862.7538442, 0.650084517),
        (865.3194468, 0.64037248),
        (868.7402502, 0.626482701),
        (871.0920525, 0.613935965),
        (873.9783553, 0.603239679),
        (875.4902283, 0.591754299),
        (878.1474595, 0.579715381),
        (880.0716614, 0.568167512),
        (882.6372639, 0.557472333),
        (884.5614658, 0.547463294),
        (886.4856677, 0.537454255),
        (888.4098696, 0.527701687),
        (890.3340715, 0.517692648),
        (892.2582734, 0.506914194),
        (894.1824753, 0.496648683),
        (896.1066773, 0.486639644),
        (898.0308792, 0.476374133),
        (899.9550811, 0.466365094),
        (901.879283, 0.456356055),
        (904.7655858, 0.44583075),
        (906.1125272, 0.436336648),
        (909.3012046, 0.424564579),
        (914.065895, 0.409750119),
        (917.7539487, 0.394491568),
        (921.6023525, 0.380853222),
        (925.8249067, 0.366679269),
        (931.8418555, 0.35267468),
        (935.5528163, 0.341425964),
        (939.4012201, 0.332008715),
        (943.2496239, 0.323018918),
        (947.0980277, 0.313174215),
        (950.9464316, 0.303543239),
        (954.7948354, 0.294339716),
        (958.6432392, 0.284495014),
        (962.491643, 0.274222859),
        (966.3400468, 0.263950703),
        (970.1884506, 0.253678548),
        (974.0368544, 0.243192667),
        (976.9231573, 0.232966579),
        (981.0922614, 0.222436845),
        (984.9406652, 0.210027425),
        (987.8269681, 0.198262508),
        (991.2477715, 0.185925807),
        (994.7907464, 0.172560763),
        (998.9140362, 0.160822106),
        (1003.140408, 0.148144224),
        (1007.710388, 0.136683396),
        (1011.238091, 0.127010782),
        (1017.331397, 0.116645384),
        (1021.179801, 0.106629701),
        (1026.952407, 0.096393647),
        (1031.955332, 0.086074759),
        (1038.497618, 0.077332132),
        (1045.232325, 0.06705001),
        (1052.929133, 0.057405746),
        (1061.106991, 0.04775982),
        (1072.491852, 0.037034188),
        (1080.83006, 0.031021057),
    ]
)

REL_FULL_SENSITIVITY_FUNC = scipy.interpolate.interp1d(
    REL_FULL_SENSITIVITY[:, 0], REL_FULL_SENSITIVITY[:, 1]
)
REL_IR_SENSITIVITY_FUNC = scipy.interpolate.interp1d(
    REL_IR_SENSITIVITY[:, 0], REL_IR_SENSITIVITY[:, 1]
)
RAT_FUNC = lambda x: REL_IR_SENSITIVITY_FUNC(x) / REL_FULL_SENSITIVITY_FUNC(x)


def smooth(x, y, delta=1, N=10):
    f = scipy.interpolate.interp1d(x, y)
    xf = np.arange(x.min(), x.max(), delta / N)
    yf = f(xf)
    cumsum = np.cumsum(np.insert(yf, 0, 0))
    rx = xf[int(N / 2) : -int(N / 2 - 1)]
    ry = (cumsum[N:] - cumsum[:-N]) / float(N)
    rf = scipy.interpolate.interp1d(rx, ry)
    return rx, ry, rf


wave_length_range = np.arange(
    max(REL_FULL_SENSITIVITY[:, 0].min(), REL_IR_SENSITIVITY[:, 0].min()),
    min(REL_FULL_SENSITIVITY[:, 0].max(), REL_IR_SENSITIVITY[:, 0].max()),
)
rx, ry, rate_smooth = smooth(
    wave_length_range, RAT_FUNC(wave_length_range), delta=20, N=10
)
diff = np.diff(ry)
diff = np.nan_to_num(diff / np.abs(diff))
diff[:-1][np.diff(diff) == 0] = 0

indexes = np.arange(len(diff))[diff.astype(bool)]
max_index_diff = np.argmax(np.diff(indexes))
lower_index = indexes[max_index_diff]
upper_index = indexes[max_index_diff + 1]

RATIO_TO_WAVELENGHT = scipy.interpolate.interp1d(
    ry[lower_index:upper_index], rx[lower_index:upper_index]
)


def luminosity_splitter(var, instance, data, send_to_board=True):
    var.default_setter(
        var=var, instance=instance, data=data, send_to_board=send_to_board
    )
    sc = struct.pack("L", data)
    instance.ch0 = struct.unpack("H", sc[:2])[0]
    instance.ch1 = struct.unpack("H", sc[2:])[0]
    try:
        instance.estimated_wavelength = RATIO_TO_WAVELENGHT(instance.ch1 / instance.ch0)
    except:
        pass


tsl2591Gain_t = ArduinoEnum(
    "tsl2591Gain_t",
    {
        0x00: ("TSL2591_GAIN_LOW", "low gain (1x)"),
        0x10: ("TSL2591_GAIN_MED", "medium gain (25x)"),
        0x20: ("TSL2591_GAIN_HIGH", "medium gain (428x)"),
        0x30: ("TSL2591_GAIN_MAX", "max gain (9876x)"),
    },
    uint8_t,
)

tsl2591IntegrationTime_t = ArduinoEnum(
    "tsl2591IntegrationTime_t",
    {
        0x00: ("TSL2591_INTEGRATIONTIME_100MS", "100 millis"),
        0x01: ("TSL2591_INTEGRATIONTIME_200MS", "200 millis"),
        0x02: ("TSL2591_INTEGRATIONTIME_300MS", "300 millis"),
        0x03: ("TSL2591_INTEGRATIONTIME_400MS", "400 millis"),
        0x04: ("TSL2591_INTEGRATIONTIME_500MS", "500 millis"),
        0x05: ("TSL2591_INTEGRATIONTIME_600MS", "600 millis"),
    },
    uint8_t,
)

tsl2591Persist_t = ArduinoEnum(
    "tsl2591Persist_t",
    {
        0: ("TSL2591_PERSIST_EVERY", "Every ALS cycle generates an interrupt"),
        2: ("TSL2591_PERSIST_ANY", "Any value outside of threshold range"),
        3: ("TSL2591_PERSIST_2", "2 consecutive values out of range"),
        4: ("TSL2591_PERSIST_3", "3 consecutive values out of range"),
        5: ("TSL2591_PERSIST_5", "5 consecutive values out of range"),
        6: ("TSL2591_PERSIST_10", "10 consecutive values out of range"),
        7: ("TSL2591_PERSIST_15", "15 consecutive values out of range"),
        8: ("TSL2591_PERSIST_20", "20 consecutive values out of range"),
        9: ("TSL2591_PERSIST_25", "25 consecutive values out of range"),
        10: ("TSL2591_PERSIST_30", "30 consecutive values out of range"),
        11: ("TSL2591_PERSIST_35", "35 consecutive values out of range"),
        12: ("TSL2591_PERSIST_40", "40 consecutive values out of range"),
        13: ("TSL2591_PERSIST_45", "45 consecutive values out of range"),
        14: ("TSL2591_PERSIST_50", "50 consecutive values out of range"),
        15: ("TSL2591_PERSIST_55", "55 consecutive values out of range"),
        16: ("TSL2591_PERSIST_60", "60 consecutive values out of range"),
    },
    uint8_t,
)


class Adafruit_TSL2591(ArduinoClass):
    class_name = "Adafruit_TSL2591"
    include = '"Adafruit_TSL2591.h"'
    begin = Function("begin", return_type=boolean)
    enable = Function("enable")
    disable = Function("disable")
    calculateLux = Function(
        "calculateLux", [(uint16_t, "ch0"), (uint16_t, "ch1")], return_type=float_
    )
    setGain = Function("setGain", [(tsl2591Gain_t, "gain")])
    setTiming = Function("setTiming", [(tsl2591IntegrationTime_t, "integration")])
    getLuminosity = Function("getLuminosity", [(uint8_t, "channel")], uint16_t)
    getFullLuminosity = Function("getFullLuminosity", return_type=uint32_t)
    getTiming = Function("getTiming", return_type=tsl2591IntegrationTime_t)
    getGain = Function("getGain", return_type=tsl2591Gain_t)

    clearInterrupt = Function("clearInterrupt")
    getStatus = Function("getStatus", return_type=uint8_t)
    registerInterrupt = Function(
        "registerInterrupt",
        [
            (uint16_t, "lowerThreshold"),
            (uint16_t, "upperThreshold"),
            (tsl2591Persist_t, "persist"),
        ],
    )


class Tsl2591(ArduinoBasicBoard):
    FIRMWARE = 15633422980183442
    adafruit_TSL2591 = Adafruit_TSL2591()

    tsl = adafruit_TSL2591("tsl", uint32_t.random())

    ch0 = python_variable(
        "ch0", type=np.float, changeable=False, is_data_point=True, save=False
    )
    ch1 = python_variable(
        "ch1", type=np.float, changeable=False, is_data_point=True, save=False
    )
    estimated_wavelength = python_variable(
        "estimated_wavelength",
        type=np.int,
        changeable=False,
        is_data_point=True,
        save=False,
    )

    luminosity = arduio_variable(
        "luminosity",
        arduino_data_type=uint32_t,
        is_data_point=True,
        arduino_setter=False,
        setter=luminosity_splitter,
        save=False,
    )
    gain = arduio_variable(
        "gain",
        arduino_data_type=uint8_t,
        allowed_values=tsl2591Gain_t,
        arduino_setter=(tsl.setGain(COMMAND_FUNCTION_COMMUNICATION_ARGUMENTS[0][0])),
        arduino_getter=(WRITE_DATA_FUNCTION(tsl.getGain(), "BYTEID")),
        is_global_var=False,
    )
    integration_time = arduio_variable(
        "integration_time",
        arduino_data_type=uint8_t,
        allowed_values=tsl2591IntegrationTime_t,  #                                  # arduino_setter="tsl.setTiming((tsl2591IntegrationTime_t) data[0]);",
        arduino_getter=(WRITE_DATA_FUNCTION(tsl.getTiming(), "BYTEID")),
        arduino_setter=(tsl.setTiming(COMMAND_FUNCTION_COMMUNICATION_ARGUMENTS[0][0])),
    )

    def __init__(self):
        super().__init__()

    def add_arduino_code(self, ad):
        ad.loop.add_call(self.luminosity.set(self.tsl.getFullLuminosity()))


if __name__ == "__main__":
    ins = Tsl2591()
    ins.create_ino()
