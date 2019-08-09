#define STARTANALOG 0
#define ENDANALOG 100
#define MAXFUNCTIONS 10
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
uint64_t firmware=15633540938822172;
uint32_t data_rate=200;
uint8_t red=0;
uint8_t green=0;
uint8_t blue=0;

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
uint8_t vifxQSmrchbl8SQtxdmi9E61V15640[sizeof(T)];
for(int i=0;i<sizeof(T);i++){
vifxQSmrchbl8SQtxdmi9E61V15640[i]=(uint8_t) (data >> (8 * i) & 0xff );
}
write_data_array(vifxQSmrchbl8SQtxdmi9E61V15640, cmd, sizeof(T));

}
void checkUUID(){
generate_checksum((uint8_t*)&id, sizeof(id));
uint16_t va9lN2R8KMbKswFKUhQhSiDCL15640;
EEPROM.get(sizeof(id), va9lN2R8KMbKswFKUhQhSiDCL15640);
if(cs != va9lN2R8KMbKswFKUhQhSiDCL15640){
id=((uint64_t)(((((uint64_t)(random()))) << 48)|((((uint64_t)(random()))) << 32)|((((uint64_t)(random()))) << 16)|((uint64_t)(random()))));
EEPROM.put(0, id);
generate_checksum((uint8_t*)&id, sizeof(id));
EEPROM.put(sizeof(id), cs);
}

}
void add_command(uint8_t cmd, uint8_t len, void (*vxSxLqABG7mKVrlI6eUgK4wjB15640)(uint8_t* data,uint8_t s)){
for(int i=0;i<MAXFUNCTIONS;i++){
if(cmds[i] == 255){
cmds[i] = cmd;
cmd_length[i] = len;
cmd_calls[i] = vxSxLqABG7mKVrlI6eUgK4wjB15640;
return ;
}
}

}
void endread(){
commandlength=0;
serialreadpos=0;

}
uint8_t get_cmd_index(uint8_t vvROtTqk6nZHyMUYoKX2PFDVt15640){
for(int i=0;i<MAXFUNCTIONS;i++){
if(cmds[i] == vvROtTqk6nZHyMUYoKX2PFDVt15640){
return i;
}
}
return 255;

}
void validate_serial_command(){
generate_checksum(serialread, (3 + serialread[2]));
if(cs == (((uint16_t)(((serialread[(3 + serialread[2])]) << 8))) + serialread[(3 + serialread[2] + 1)])){
uint8_t vfVWuqS7A5cP18uXNBxJ1QGKH15640=get_cmd_index(serialread[1]);
if(vfVWuqS7A5cP18uXNBxJ1QGKH15640 != 255){
uint8_t vAQX7Ql1e4ak3I03162uvTWQK15640[serialread[2]];
memcpy(vAQX7Ql1e4ak3I03162uvTWQK15640,&serialread[3],serialread[2]);
cmd_calls[vfVWuqS7A5cP18uXNBxJ1QGKH15640](vAQX7Ql1e4ak3I03162uvTWQK15640, serialread[2]);
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
void set_red_4(uint8_t* data, uint8_t s){
red=data[0];
}
void get_red_5(uint8_t* data, uint8_t s){
write_data(red,5);
}
void set_green_6(uint8_t* data, uint8_t s){
green=data[0];
}
void get_green_7(uint8_t* data, uint8_t s){
write_data(green,7);
}
void set_blue_8(uint8_t* data, uint8_t s){
blue=data[0];
}
void get_blue_9(uint8_t* data, uint8_t s){
write_data(blue,9);
}


void dataloop(){

}

void loop(){
readloop();
ct=millis();
if(((ct - lastdata) > data_rate && identified)){
dataloop();
lastdata=ct;
}
analogWrite(3,red);
analogWrite(5,green);
analogWrite(6,blue);

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
add_command(4, 1, set_red_4);
add_command(5, 0, get_red_5);
add_command(6, 1, set_green_6);
add_command(7, 0, get_green_7);
add_command(8, 1, set_blue_8);
add_command(9, 0, get_blue_9);
analogWrite(3,OUTPUT);
analogWrite(5,OUTPUT);
analogWrite(6,OUTPUT);

}
