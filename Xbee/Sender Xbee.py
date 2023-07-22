import csv
import serial
from xbee import XBee
import time

serialport = serial.Serial('COM port to which the xbee is connected', 9600) # Serial Port Configuration
XBee = XBee(serialport)
dest_addr = b'\x00\x00'


num_frames = 10000
total_time = 0 
num_frames_received = 0  
num_frames_lost = 0  

# Open CSV file for writing
with open('fffffinal 100b,115200 1ms.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

   
    writer.writerow(['Frame Number', 'Round-Trip Time in second', 'Frame Received', 'Lost Frame Content'])

    for i in range(num_frames):
        # Send frame
        frame = bytes([1,2,3] * 20)# 60-byte frames
        start_time = time.time()  # Record the time just before sending
        XBee.tx(dest_addr=dest_addr, data=frame)
        print(f'Sent frame {i+1}/{num_frames}')
        time.sleep(0.001) # Wait for 1 ms 

        # Receive response
        response = XBee.wait_read_frame()
        end_time = time.time()  
        print(f'Received response {i+1}/{num_frames}: {(response["rf_data"])}')
        rtt = end_time - start_time  # Calculate the round-trip times
        total_time += rtt 
        print(f'Delay: {rtt} s')

        # Check if the received frame is the same as the sent frame(if loss)
        if response["rf_data"] == frame:
            frame_received = 'Yes'
            num_frames_received += 1
        else:
            frame_received = 'No'
            num_frames_lost += 1
            lost_frame_content = response["rf_data"]
            print(f'Lost frame content: {lost_frame_content}')
            writer.writerow([i+1, rtt, frame_received, lost_frame_content])
            continue

        
        writer.writerow([i+1, rtt, frame_received, ''])

serialport.close()

Total_Time = total_time
avg_rtt = total_time / num_frames
packet_delivery_ratio = num_frames_received / num_frames
print(f'Average delay: {avg_rtt} s')
print(f'Total time : {total_time} s')
print(f'Packet Delivery Ratio: {packet_delivery_ratio}')
if num_frames_lost == 0:
    print("No frames were lost in the cyclical communication.")
else:
    print(f'{num_frames_lost} frames were lost in the cyclical communication.')
