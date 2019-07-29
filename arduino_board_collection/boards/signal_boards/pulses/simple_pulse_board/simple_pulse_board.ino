#define STARTANALOG 0
#define ENDANALOG 100
#define MAXFUNCTIONS 12
#define BAUD 9600
#define SERIALARRAYSIZE 13

#include <EEPROM.h>

uint32_t lastdata=0;
uint32_t ct;
uint8_t c;
uint16_t cs;
uint64_t id;
bool identified=0;
uint8_t serialreadpos=0;
uint8_t commandlength=0;
uint8_t writedata[SERIALARRAYSIZE];
uint8_t serialread[SERIALARRAYSIZE];
uint8_t cmds[MAXFUNCTIONS];
uint8_t cmd_length[MAXFUNCTIONS];
void (*cmd_calls[MAXFUNCTIONS])(uint8_t* data,uint8_t s);
uint64_t firmware=15627604053828192;
uint32_t data_rate=200;
uint8_t pulse_type=1;
uint16_t wavelength=1000;
uint16_t current_val=0;
bool pulsing=0;
double pulse_pos=0;
uint16_t max_current_val=-1;

uint16_t generate_checksum(uint8_t* data, uint8_t count){
uint16_t sum1=0;
uint16_t sum2=0;
for(int i=0;i<count;i++){
sum1=((sum1 + data[i]) % 255);
sum2=((sum1 + sum2) % 255);
}
cs=(sum2 << 8) | sum1;

}
void write_data_array(uint8_t* data, uint8_t cmd, uint8_t len){
writedata[0] = 2;
writedata[1] = cmd;
writedata[2] = len;
for(int i=0;i<len;i++){
writedata[(3 + i)] = data[i];
}
generate_checksum(writedata, (len + 3));
writedata[(3 + len)] = cs >> 8;
writedata[(3 + len + 1)] = cs >> 0;
Serial.write(writedata, (3 + len + 2));

}
template< typename T> void write_data(T data, uint8_t cmd){
uint8_t vTNsp12LZAQ0WuC8ScAVTKbDu15640[sizeof(T)];
for(int i=0;i<sizeof(T);i++){
vTNsp12LZAQ0WuC8ScAVTKbDu15640[i]=(uint8_t) (data >> (8 * i) & 0xff );
}
write_data_array(vTNsp12LZAQ0WuC8ScAVTKbDu15640, cmd, sizeof(T));

}
void checkUUID(){
generate_checksum((uint8_t*)&id, sizeof(id));
uint16_t v7OhpjOcEMxsrCgHBf8WKhs7Y15640;
EEPROM.get(sizeof(id), v7OhpjOcEMxsrCgHBf8WKhs7Y15640);
if(cs != v7OhpjOcEMxsrCgHBf8WKhs7Y15640){
id=((uint64_t)(((((uint64_t)(random()))) << 48)|((((uint64_t)(random()))) << 32)|((((uint64_t)(random()))) << 16)|((uint64_t)(random()))));
EEPROM.put(0, id);
generate_checksum((uint8_t*)&id, sizeof(id));
EEPROM.put(sizeof(id), cs);
}

}
void add_command(uint8_t cmd, uint8_t len, void (*vYqqVzFKeNfGwiqTqpxFUi3f215640)(uint8_t* data,uint8_t s)){
for(int i=0;i<MAXFUNCTIONS;i++){
if(cmds[i] == 255){
cmds[i] = cmd;
cmd_length[i] = len;
cmd_calls[i] = vYqqVzFKeNfGwiqTqpxFUi3f215640;
return ;
}
}

}
void endread(){
commandlength=0;
serialreadpos=0;

}
uint8_t get_cmd_index(uint8_t vkxwevPS43nfZSmqbPahioUWT15640){
for(int i=0;i<MAXFUNCTIONS;i++){
if(cmds[i] == vkxwevPS43nfZSmqbPahioUWT15640){
return i;
}
}
return 255;

}
void validate_serial_command(){
generate_checksum(serialread, (3 + serialread[2]));
if(cs == (((uint16_t)(((serialread[(3 + serialread[2])]) << 8))) + serialread[(3 + serialread[2] + 1)])){
uint8_t vkH2BOsDndRdWKrQ8llrTo8Ro15640=get_cmd_index(serialread[1]);
if(vkH2BOsDndRdWKrQ8llrTo8Ro15640 != 255){
uint8_t vBfm9bzbgMrpIqlGeqmyTgTX315640[serialread[2]];
memcpy(vBfm9bzbgMrpIqlGeqmyTgTX315640,&serialread[3],serialread[2]);
cmd_calls[vkH2BOsDndRdWKrQ8llrTo8Ro15640](vBfm9bzbgMrpIqlGeqmyTgTX315640, serialread[2]);
}
}

}
void readloop(){
while(Serial.available() > 0){
c=Serial.read();
serialread[serialreadpos] = c;
if(serialreadpos == 0){
if(c == 2){
}
else {
endread();
continue;
}
}
else {
if(serialreadpos == 2){
commandlength=c;
}
else if((serialreadpos - commandlength) > (3 + 1)){
endread();
continue;
}
else if((serialreadpos - commandlength) == (3 + 1)){
validate_serial_command();
endread();
continue;
}
}
serialreadpos++;
}

}
void identify_0(uint8_t* data, uint8_t s){
identified=data[0];write_data(id,0);
}
void get_firmware_1(uint8_t* data, uint8_t s){
write_data(firmware,1);
}
void set_data_rate_2(uint8_t* data, uint8_t s){
uint32_t temp;memcpy(&temp,data,4);data_rate=temp;
}
void get_data_rate_3(uint8_t* data, uint8_t s){
write_data(data_rate,3);
}
void set_pulse_type_4(uint8_t* data, uint8_t s){
pulse_type=data[0];
}
void get_pulse_type_5(uint8_t* data, uint8_t s){
write_data(pulse_type,5);
}
void set_wavelength_6(uint8_t* data, uint8_t s){
uint16_t temp;memcpy(&temp,data,2);wavelength=temp;
}
void get_wavelength_7(uint8_t* data, uint8_t s){
write_data(wavelength,7);
}
void set_current_val_8(uint8_t* data, uint8_t s){
uint16_t temp;memcpy(&temp,data,2);current_val=temp;
}
void get_current_val_9(uint8_t* data, uint8_t s){
write_data(current_val,9);
}
void set_pulsing_10(uint8_t* data, uint8_t s){
pulsing=data[0];
}
void get_pulsing_11(uint8_t* data, uint8_t s){
write_data(pulsing,11);
}


void dataloop(){
write_data(current_val, 9);

}

void loop(){
readloop();
ct=millis();
if(((ct - lastdata) > data_rate && identified)){
dataloop();
lastdata=ct;
}
if(pulsing){
pulse_pos=((ct % wavelength)/(1.0 * wavelength));
if(pulse_type == 0){
if(0.5 >= pulse_pos){
current_val = max_current_val;
}
else {
current_val = 0;
}
}
else if(pulse_type == 1){
current_val = (max_current_val * ((1 + sin((2 * pulse_pos * PI)))/2));
}
analogWrite(6,map(current_val, 0, max_current_val, 0, 255));
}

}

void setup(){
Serial.begin(BAUD);
EEPROM.get(0, id);
for(int i=STARTANALOG;i<ENDANALOG;i++){
randomSeed((max(1,analogRead(i)) * random()));
}
checkUUID();
for(int i=0;i<MAXFUNCTIONS;i++){
cmds[i]=255;
}
ct=millis();
add_command(0, 1, identify_0);
add_command(1, 0, get_firmware_1);
add_command(2, 4, set_data_rate_2);
add_command(3, 0, get_data_rate_3);
add_command(4, 1, set_pulse_type_4);
add_command(5, 0, get_pulse_type_5);
add_command(6, 2, set_wavelength_6);
add_command(7, 0, get_wavelength_7);
add_command(8, 2, set_current_val_8);
add_command(9, 0, get_current_val_9);
add_command(10, 1, set_pulsing_10);
add_command(11, 0, get_pulsing_11);

}
