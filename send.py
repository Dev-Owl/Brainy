import time
import sys
import RPi.GPIO as GPIO

#Code for ALDI 433mhz sockets
a_on   =  '000110111000101001010011300010010010001101010001102'
a_off  = '000110111000101001010011300011010111100010100001102'
b_on   =  '00011011100010100101001130001010001010000000010102'
b_off  = '00011011100010100101001130001000111101000001110102'
c_on   =  '00011011100010100101001130001011000001001110100012'
c_off  = '00011011100010100101001130001101110001010010100012'
d_on   =  '0001101110001010010100113000100011110100000111000'
d_off  = '00011011100010100101001130001100010010100111110002'
m_on   = '00011011100010100101001130001011100011101011111012'
m_off  = '00011011100010100101001130001101110001010010111012'

#times used by the code above, 1 is short_on + long_off etc
long_on   = 0.000921
short_off = 0.000601

short_on  = 0.000414
long_off  = 0.001115

end_on    = 0.002931
end_off   = 0.007269

end_off2  = 0.002393

#How often should the script send the sequence
retries = 6
#Pin to send out the data
pin = 27

def send(code):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0) #Set pin to 0 and wait just to make sure we start in the same way everytime
    time.sleep(0.1)
    for t in range(retries):
        for i in code:
            if   i == '0':
                GPIO.output(pin, 1)
                time.sleep(long_on)
                GPIO.output(pin, 0)
                time.sleep(short_off)
            elif i == '1':
                GPIO.output(pin, 1)
                time.sleep(short_on)
                GPIO.output(pin, 0)
                time.sleep(long_off)
            elif i == '2':
                GPIO.output(pin, 1)
                time.sleep(end_on)
                GPIO.output(pin, 0)
                time.sleep(end_off)
            elif i == '3':
                GPIO.output(pin, 1)
                time.sleep(short_on)
                GPIO.output(pin, 0)
                time.sleep(end_off2)
            else:
                continue
       
    GPIO.cleanup()#Clean up and done

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('send(' + str(argument) + ')')

