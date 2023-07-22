import serial
from xbee import XBee # Serial Port Configuration

serialport=serial.Serial('COM port to which the xbee is attached', 9600)
src_addr = b'x00x00'
XBEE = XBee (serialport) 
try:
  while True:
# Wait for a massage and inspect the sender 
    resp=XBEE.wait_read_frame() 
    if resp['source_addres']==src_addr: Frame=resp['rf_data']
    XBEE.tx(destination_addr=resp['source_addr'], data=Frame)
    print(f'Received Frame: Frame')
finally:
 serialport.close() 
