sudo modprobe can  
sudo modprobe can_raw  
sudo modprobe slcan

USB_NUMBER=$(ls /dev/ttyUSB* | grep -o -E '[0-9]+')
sudo slcand -o -s8 -t hw -S 3000000 /dev/ttyUSB$USB_NUMBER slcan0
sudo ip link set up slcan0  
candump slcan0 
