import serial
import argparse

VERBOSE = False
SKIPCRC = False

def toByte(raw):
    result = "".join(str(v) for v in raw)
    return int(result,2)

def checksum(data):
    byte1 = toByte(data[:8])
    byte2 = toByte(data[8:16])
    byte3 = toByte(data[16:24])
    byte4 = toByte(data[24:32])
    byte5 = toByte(data[32:40])
    printv( "Byte values {0},{1},{2},{3},{4}".format(byte1,byte2,byte3,byte4,byte5))
    return ((byte1+byte2+byte3+byte4-byte5) %256) == 0

def parseData(data):
    printv("----------------------------------------")
    printv("Got: {0}".format(data))
    printv("Total bit {0}".format(len(data)))
    if len(data) >= 40:
        if checksum(data) or SKIPCRC:
            rawID = toByte(data[:8])
            batteryEmpty = data[8] == "1"
            sendButton = data[9] == "1"
            chanel =toByte(data[10:12])
            temperature = round(((( float(toByte(data[12:24]))/10) - 90) -32) * 5/9,2)
            humidity = toByte(data[24:32])
            print "ID:{0} Battery:{1} SendButton:{2} Chanel:{3} Temperatur:{4} Humidity:{5}".format(rawID,batteryEmpty,sendButton,chanel,temperature,humidity)
        else:
            printv("Checksum failed")
        
    else:
        printv("Message is too short")
    printv("----------------------------------------")
def printv(msg):
    if(VERBOSE):
        print msg

if __name__ == '__main__':
    ap= argparse.ArgumentParser(description='Communicate via serial interface and get values from remote sensor')
    ap.add_argument("-port", action='store', help="name of serial port to open")
    ap.add_argument("-verbose", action='store_true',help="verbose output flag")
    ap.add_argument("-skipcrc", action='store_true',help="skip crc check, danger")
    ap.add_argument("-parse", action='store', help="parse message and quit")
    args= ap.parse_args()
    
    if args.port == None and args.parse == None:
        print "No port set, use -port to configure serial port"
        exit(0)
    VERBOSE = args.verbose
    SKIPCRC = args.skipcrc
    if args.parse != None:
        parseData(args.parse)
        exit(0)
        

    arduino = serial.Serial(args.port,115200,timeout=.1)
    while True:
        data = arduino.readline()[:-2]
        if data:
            parseData(data)

