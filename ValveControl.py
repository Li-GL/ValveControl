import serial
import serial.tools.list_ports
import time
import datetime
import os
import csv

################ Check Com Port ##################################
def serial_ports():

    ports = list(serial.tools.list_ports.comports())

    port_all =""

    # return the port if 'USB' is in the description
    for port_no, description, address in ports:
        if 'Arduino' in description:
            port_all = port_all+' '+port_no
    return port_all.split()
################ Write data to CSV ###############################
def writeToCSV(valvestatus):
    ########## Write ReadTem to file
    current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    current_time_filename = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    filename_1 = 'Valve' + 'Status' + current_time_filename + '.csv'
    #####creat folder "ValveControl" in current path
    current_path = os.getcwd()
    save_path = os.path.join(current_path, 'ValveControl')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = os.path.join(save_path, filename_1)

    if not os.path.exists(filename):
        with open(filename, 'w') as csvfile:
            fieldnames =  ['date', 'valve (note two valves have different diameter, thin or thick one)']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
    ####  write data to csv file
    with open(filename, 'a') as csvfile:
        fieldnames = ['date', 'valve (note two valves have different diameter, thin or thick one']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writerow({'date': current_time, 'valve (note two valves have different diameter, thin or thick one': str(valvestatus)})

################ Main function####################################
##Input time interval
print 'Time interval (min): '
timeInterval = float(raw_input())*60
##To determine ComPort
ComPort = serial_ports()
ComPort = ''.join(ComPort)
print 'Connected to port ' + ComPort
ser = serial.Serial(port=ComPort, baudrate=9600)

while True:
    try:
        while True:

            ## Set for Arduino, refer to http://stackoverflow.com/questions/2301127/pyserial-app-runs-in-shell-by-not-py-script
            time.sleep(0.5)
            ser.setDTR(level=0)
            time.sleep(0.5)

            current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

            ## Control Valve open
            ser.write(b'TurnOnDevice1\n')
            ValveStatus = '#76_thin open'
            print current_time + '\t' + str(ValveStatus)
            writeToCSV(ValveStatus)
            time.sleep(timeInterval)

            ## Set for Arduino
            ser.setDTR(level=0)

            #### Control Valve open
            ser.write(b'TurnOffDevice1\n')
            ValveStatus = '#76_thin close'
            current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            print current_time + '\t' + str(ValveStatus)
            writeToCSV(ValveStatus)
            time.sleep(timeInterval-1)


    except serial.SerialException:
         try:
             ser = serial.Serial(port=ComPort, baudrate=9600)
         except:
             print 'Seems lost connection, trying reconnect!!!'
             time.sleep(5)
    else:
        print 'Something wrong, please check the whole setup!!!'
        time.sleep(5)






