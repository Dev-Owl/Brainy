from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO
import argparse
import io, json, time
import jsonpickle

#Globals and defaults
HIGH = 0 #Position in time tuple
LOW  = 1
WORKING_DATA = [[], []]  #[[time], [signal]]
MAX_DURATION = 5 #Default time to record data
RECEIVE_PIN = 27 #Input pin
TRANSMITTER_PIN = 22 #Output pin
HIGH_OFFSET = 0.00005 #Default offsets for time generations 
LOW_OFFSET  = 0.00005
VERBOSE = False #Verbose loging setting

'''
    Class to store the high and low times for a signal
'''
class Signal:
    def __init__(self, high, low):
        self.high = high
        self.low  = low
    def __str__(self):
       return "{high:{0:.8f},low:{1:.8f}}".format( float(self.high),float(self.low))
    def key(self):
        return (self.high, self.low)
'''
    Result for a Signal including how often it occoured and the encoded symbol
'''
class Reading:
    def __init__(self,amount,code):
        self.amount = amount
        self.code = code
'''
    Json file structure for a complete transmit file include encoded message and times
'''
class TransmitFile:
    def __init__(self,encodings,protocol):
        self.encoding = encodings
        self.protocol = protocol
    
#Read raw signal data from a file
def read_file(path):
    return json.load(open(path))

#write raw signal data to a file
def write_file(path):
    vprint("Writing to file",True)
    with open(path, 'w') as f:
        json.dump(WORKING_DATA,f)
#Record data from the receiver
def record_data():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    beginning_time = datetime.now()
    vprint('Started recording', True)
    while cumulative_time < MAX_DURATION: # Record for fixed time default 5s
        time_delta= datetime.now() - beginning_time
        WORKING_DATA[0].append(time_delta)
        WORKING_DATA[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    vprint('Ended recording', True)
    print vprint("{0},samples recorded".format( len(WORKING_DATA[0])), True)
    GPIO.cleanup()

    vprint('Processing', True)
    for i in range(len(WORKING_DATA[0])):
        WORKING_DATA[0][i]= WORKING_DATA[0][i].seconds + WORKING_DATA[0][i].microseconds/1000000.0
#Plot recorded data to diagram
def simple_plot():
    vprint('Plotting', True)
    pyplot.plot(WORKING_DATA[0], WORKING_DATA[1])
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.show()
#Group signal times to avoid issues with too many records
def group_times(data, newkey, high):
    for k in data:
        if high:
            if abs(float(k[HIGH]) - float(newkey)) <= HIGH_OFFSET:
                return k[HIGH]
        else:
            if abs(float(k[LOW]) - float(newkey)) <= LOW_OFFSET:
                return k[LOW]
    return newkey

def time_pattern(screen, encode):
    vprint("Pattern search started", True)
    pattern = {} # {{(Signal),(Amount/Encoded)}}
    state = 0 #current state in loop
    change_high_time = 0 #time for the change
    encoder_counter = 0 #counter to genereate number code for msg
    encoded_msg = [] #encoded message result
    change_low_time = 0
    current_signal = Signal(0 ,0)
    for i in range(len(WORKING_DATA[1])):
        if state <> WORKING_DATA[1][i]:
            if WORKING_DATA[1][i] == 1:
                #Check if low state time has a value
                if change_low_time <> 0:
                    #build low time for last change
                    current_signal.low = group_times(pattern, WORKING_DATA[0][i]-change_low_time, False)
                    if current_signal.low <> 0 and current_signal.high <> 0:
                        #signal ready to add
                        key = current_signal.key()
                        if key in pattern:
                            pattern[key].amount +=1 
                            encoded_msg.append( pattern[key].code)
                        else:
                            pattern[key] = Reading(1, str(encoder_counter))
                            encoded_msg.append( pattern[key].code)
                            encoder_counter += 1
                        current_signal = Signal(0, 0) # reset current signal to new
                        change_low_time = 0
                    else:
                        print "Error something went wrong"
                #High state change track high time
                change_high_time = WORKING_DATA[0][i]
            else:
                if change_high_time <> 0:
                    #build high time for last change
                    current_signal.high = group_times(pattern, WORKING_DATA[0][i]-change_high_time, True)
                #change to low track last low time
                change_low_time = WORKING_DATA[0][i]
            state = WORKING_DATA[1][i]
    vprint("Pattern search done",True)
    vprint("Processing results",True)
    if screen:
        for k,v in sorted(pattern.items(), key=lambda x:x[1].amount):
            print "Pattern high {0:.8f} low {1:.8f} occoured {2}".format(float(k[HIGH]), float(k[LOW]), v.amount)
    if encode:
        print "On time encoded:"
        for k,v in sorted(pattern.items(), key=lambda x:x[1].amount):
            print "Pattern high {0:.8f} low {1:.8f} encoded as {2} occoured {3}".format(float(k[HIGH]), float(k[LOW]), v.code, v.amount)
        print ",".join(str(v) for v in encoded_msg)
    return (pattern, encoded_msg)
#Print a message if verbose mode is on    
def vprint(message, info):
    if info and VERBOSE or not info:
        print message

#Write the transmitter file to disk
def create_transmitter_file():
    global WORKING_DATA
    if len(WORKING_DATA[0]) == 0:
        print "No data loaded, choose: 1:record 2:read"
        selection = raw_input("Select:")
        if selection == "1":
            record_data()
        elif selection == "2":
            path = raw_input("Path to file:")
            WORKING_DATA= read_file(path)
        else:
            print "Invalid input"
            return
    if len(WORKING_DATA[0]) == 0:
        print "No data loaded"
        return
    
    data = time_pattern(False,False)
    #wirte file
    transmitFile = TransmitFile( create_encode(data), data[1])
    save_path = raw_input("Path to save file:")
    with open(save_path, 'w') as f:
        f.write(jsonpickle.encode( transmitFile))
    print "File created, use the -transmit option to send this file"
#Create the encode dic that is used for sending data
def create_encode(data):
    encode_times = {}
    for k,v in data[0].items():
        encode_times[v.code] = k
    return encode_times
#Skip the transmit file and send the data directly     
def fast_send():
    global WORKING_DATA
    data = time_pattern(False, False)
    #wirte file
    transmitFile = TransmitFile( create_encode(data), data[1])
    send(transmitFile)
#Send data based on the TransmitFile class
def send(data):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT)
    GPIO.output(TRANSMITTER_PIN, 0)
    for t in range(1):
        for e in data.protocol:
            times = data.encoding[e]
            GPIO.output(TRANSMITTER_PIN, 1)
            time.sleep(times[HIGH])
            GPIO.output(TRANSMITTER_PIN, 0)
            time.sleep(times[LOW])
    GPIO.cleanup()
#Open the a transmit file and send it
def transmit(file):
    f = open(file, "r") 
    send(jsonpickle.decode(f.read()))
    

if __name__ == '__main__':
    ap= argparse.ArgumentParser(description='Tool to help and analyze 433mhz signals')
    ap.add_argument("-rec", action='store_true', help="record signal")
    ap.add_argument("-read", action='store',help="read data from file, provide path")
    ap.add_argument("-write", action='store', help="write data to file")
    ap.add_argument("-plot", action='store_true', help="plot data")
    ap.add_argument("-i_pin", action='store', help="input pin of the receiver, default: 27", default=27)
    ap.add_argument("-duration", action='store', help="duration in seconds, default: 5s", default=5)
    ap.add_argument("-l_offset", action='store', help="low offset for signal grouping, default 0.00005s", default=0.00005)
    ap.add_argument("-h_offset", action='store', help="high offset for signal grouping, default 0.00005s", default=0.00005)
    ap.add_argument("-pattern",action='store_true', help="try to find singal time patterns")
    ap.add_argument("-encode",action='store_true', help="try to encode signal")
    ap.add_argument("-o_pin", action='store', help="output pin for transmitter, default: 22",default=22)
    ap.add_argument("-verbose",action='store_true', help="display configuration on start", default=False)
    ap.add_argument("-create", action='store_true', help="create a new transmitter file based on the loaded data")
    ap.add_argument("-fastsend", action='store_true', help="analyse build command and send result in one step")
    ap.add_argument("-transmit",action="store", help="send a transmit file")
    args= ap.parse_args()
    VERBOSE = args.verbose
    
    if not(args.rec) and args.read==None and args.create == False and args.transmit == None:
        print "Either record or read from a file"
        exit(0)
        
    if args.rec and args.read <> None:
        print "Recording and reading at the same time will no work"
        exit(0)
        
    if args.i_pin <> None:
        #override the pin where the receiver is connected to
        RECEIVE_PIN= int(args.i_pin)
        vprint( "Using pin {0} for inputs".format(RECEIVE_PIN), True)
    if args.o_pin <> None:
        TRANSMITTER_PIN = int (args.o_pin)
        vprint( "Using pin {0} for outputs".format(TRANSMITTER_PIN), True)
    if args.duration <> None:
        #override the default time for recording actions
        MAX_DURATION= int(args.duration)
        vprint( "Recording set to {0} seconds".format(MAX_DURATION), True)
    if args.l_offset <> None:
        LOW_OFFSET = float(args.l_offset)
        vprint( "Low offset set to {0:.8f} seconds".format(LOW_OFFSET), True)
    if args.h_offset <> None:
        HIGH_OFFSET = float(args.h_offset)
        vprint( "High offset set to {0:.8f} seconds".format(HIGH_OFFSET), True)
    
    if args.read <> None:
        if args.read== '':
            args.read= "./data.json"
        vprint("Reading from file: {0}".format(args.read), True)
        WORKING_DATA= read_file(args.read)
        vprint('{0},samples recorded'.format(len(WORKING_DATA[0])),True)
        vprint("Finished reading",True)
        
    if args.rec:
        record_data()
    
    if args.write <> None:
        if args.write== '':
            args.write= "./data.json"
        write_file(args.write)
    
    if args.plot:
        simple_plot()
    if args.pattern or args.encode:
        if len(WORKING_DATA[0]) == 0:
            print "No data loaded, either use rec or read to get data"
            exit(0)
        time_pattern(args.pattern, args.encode)
    if args.fastsend:
        fast_send()
    if args.create:
        create_transmitter_file()
    if args.transmit <> None:
        transmit(args.transmit)
        
