#define STARTANALOG 0
#define ENDANALOG 100
#define STARTBYTE 2
#define STARTBYTEPOSITION 0
#define COMMANDBYTEPOSITION 1
#define LENBYTEPOSITION 2
#define DATABYTEPOSITION 3
#define MAXFUNCTIONS 15
#define SERIALARRAYSIZE 13
#define BAUD 9600
#define LED_PIN_RED 3
#define LED_PIN_GREEN 5
#define LED_PIN_BLUE 6
#include "Adafruit_TSL2591.h"
#include <EEPROM.h>
uint64_t firmware = 1563437279774598;
uint32_t data_rate = 200;
uint32_t luminosity = 0;
uint8_t red = 0;
uint8_t green = 0;
uint8_t blue = 0;
uint8_t writedata[SERIALARRAYSIZE];
uint8_t serialread[SERIALARRAYSIZE];
uint8_t serialreadpos = 0;
uint8_t commandlength = 0;
uint8_t cmds[MAXFUNCTIONS ];
uint8_t cmd_length[MAXFUNCTIONS];
void (*cmd_calls[MAXFUNCTIONS])(uint8_t* data, uint8_t s);
uint32_t lastdata = 0;
uint32_t ct;
uint8_t c;
bool identified = false;
Adafruit_TSL2591 tsl = Adafruit_TSL2591(-543679036);
uint16_t generate_checksum(uint8_t* data, int count){
uint16_t sum1 = 0;
uint16_t sum2 = 0;
for (int index = 0; index < count; ++index ) {
sum1 = (sum1 + data[index]) % 255;
sum2 = (sum2 + sum1) % 255;
}
return (sum2 << 8) | sum1;
}
void write_data_array(uint8_t* data, uint8_t cmd, uint8_t len){
writedata[STARTBYTEPOSITION] = STARTBYTE;
writedata[COMMANDBYTEPOSITION] = cmd;
writedata[LENBYTEPOSITION] = len;
for (uint8_t i = 0; i < len; i++) {
writedata[DATABYTEPOSITION + i] = data[i];
}uint16_t cs = generate_checksum(writedata, len + DATABYTEPOSITION);
writedata[DATABYTEPOSITION + len] = cs >> 8;
writedata[DATABYTEPOSITION + len + 1] = cs >> 0;
Serial.write(writedata, len + DATABYTEPOSITION + 2);
}
template< typename T> void write_data(T data, uint8_t cmd){
uint8_t d[sizeof(T)];
for (uint8_t i = 0;i<sizeof(T) ; i++) {
d[i] = (uint8_t) (data >> (8 * i) & 0xff );
}
write_data_array(d, cmd, sizeof(T));
}
uint64_t get_id(){
uint64_t id;
EEPROM.get(0, id);
return id;
}
void checkUUID(){
uint64_t id = get_id();
uint16_t cs = generate_checksum((uint8_t*)&id, sizeof(id));
uint16_t cs2;
EEPROM.get(sizeof(id), cs2);
if (cs != cs2) {
id = (uint64_t)((((uint64_t)random()) << 48) | (((uint64_t)random()) << 32) | (((uint64_t)random()) << 16) | (((uint64_t)random())));
EEPROM.put(0, id);
EEPROM.put(sizeof(id), generate_checksum((uint8_t*)&id, sizeof(id)));
}
}
void add_command(uint8_t cmd, uint8_t len, void (*func)(uint8_t* data, uint8_t s)){
for (uint8_t i = 0; i < MAXFUNCTIONS; i++ ) {
if (cmds[i] == 255) {
cmds[i] = cmd;
cmd_length[i] = len;
cmd_calls[i] = func;
return;
}
}
}
void endread(){
commandlength = 0;
serialreadpos = STARTBYTEPOSITION;
}
uint8_t get_cmd_index(uint8_t cmd){
for (uint8_t i = 0; i < MAXFUNCTIONS; i++ ) {
if (cmds[i] == cmd) {
return i;
}
}
return 255;}
void validate_serial_command(){
if(generate_checksum(serialread, DATABYTEPOSITION + serialread[LENBYTEPOSITION]) == (uint16_t)(serialread[DATABYTEPOSITION + serialread[LENBYTEPOSITION]] << 8) + serialread[DATABYTEPOSITION + serialread[LENBYTEPOSITION]+1]){
uint8_t cmd_index = get_cmd_index(serialread[COMMANDBYTEPOSITION]);
if(cmd_index != 255){
uint8_t data[serialread[LENBYTEPOSITION]];
memcpy(data,&serialread[DATABYTEPOSITION],serialread[LENBYTEPOSITION]);
cmd_calls[cmd_index](data,serialread[LENBYTEPOSITION]);
}
}
}
uint64_t readloop(){
while(Serial.available() > 0) {
c = Serial.read();
serialread[serialreadpos] = c;
if (serialreadpos == STARTBYTEPOSITION) {
if (c == STARTBYTE) {
} else {
endread();
continue;
}
}
else {
if (serialreadpos == LENBYTEPOSITION) {
commandlength = c;
} else if (serialreadpos - commandlength > DATABYTEPOSITION + 1 ) { //stx cmd len cs cs (len = 0; pos = 4)
endread();
continue;
}
else if (serialreadpos - commandlength == DATABYTEPOSITION + 1) {
validate_serial_command();
endread();
continue;
}
}
serialreadpos++;
}
}
void identify_0(uint8_t* data, uint8_t s){
identified=data[0];uint64_t id = get_id();write_data(id,0);}
void get_firmware_1(uint8_t* data, uint8_t s){
write_data(firmware,1);}
void set_data_rate_2(uint8_t* data, uint8_t s){
uint32_t temp;memcpy(&temp,data,4);data_rate=temp;}
void get_data_rate_3(uint8_t* data, uint8_t s){
write_data(data_rate,3);}
void get_luminosity_4(uint8_t* data, uint8_t s){
write_data(luminosity,4);}
void set_gain_5(uint8_t* data, uint8_t s){
tsl.setGain((tsl2591Gain_t) data[0]);}
void get_gain_6(uint8_t* data, uint8_t s){
write_data(tsl.getGain(),6);}
void set_integration_time_7(uint8_t* data, uint8_t s){
tsl.setTiming((tsl2591IntegrationTime_t) data[0]);}
void get_integration_time_8(uint8_t* data, uint8_t s){
write_data(tsl.getTiming(),8);}
void set_red_9(uint8_t* data, uint8_t s){
red=data[0];}
void get_red_10(uint8_t* data, uint8_t s){
write_data(red,10);}
void set_green_11(uint8_t* data, uint8_t s){
green=data[0];}
void get_green_12(uint8_t* data, uint8_t s){
write_data(green,12);}
void set_blue_13(uint8_t* data, uint8_t s){
blue=data[0];}
void get_blue_14(uint8_t* data, uint8_t s){
write_data(blue,14);}

void dataloop(){
write_data(luminosity,4);

}

void loop(){
readloop();
ct = millis();
if(ct-lastdata>data_rate && identified){
dataloop();
lastdata=ct;
}
if(identified){luminosity=tsl.getFullLuminosity();
}analogWrite(LED_PIN_RED, red);analogWrite(LED_PIN_GREEN, green);analogWrite(LED_PIN_BLUE, blue);
}

void setup(){
Serial.begin(BAUD);
while (!Serial) {;}
for (int i = STARTANALOG; i < ENDANALOG; i++) {
randomSeed(analogRead(i)*random());
}
checkUUID();
for (uint8_t i = 0; i < MAXFUNCTIONS; i++ ) {
cmds[i] = 255;
}
ct = millis();
add_command(0, 1, identify_0);
add_command(1, 0, get_firmware_1);
add_command(2, 4, set_data_rate_2);
add_command(3, 0, get_data_rate_3);
add_command(4, 0, get_luminosity_4);
add_command(5, 1, set_gain_5);
add_command(6, 0, get_gain_6);
add_command(7, 1, set_integration_time_7);
add_command(8, 0, get_integration_time_8);
add_command(9, 1, set_red_9);
add_command(10, 0, get_red_10);
add_command(11, 1, set_green_11);
add_command(12, 0, get_green_12);
add_command(13, 1, set_blue_13);
add_command(14, 0, get_blue_14);
pinMode(LED_PIN_RED, OUTPUT);pinMode(LED_PIN_GREEN, OUTPUT);pinMode(LED_PIN_BLUE, OUTPUT);
}
