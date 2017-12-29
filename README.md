# Brainy
Collection of scripts, applications and tools that I use in my "smart" home system I´m currently building

# Scripts

## whoisthere.py
Simple and dirty script to read connected devices from the webfrontend of my netgear router and prompt as JSON. Including IP,Name and MAC.
Requires the Python module: 
+ https://github.com/requests/requests
+ https://github.com/djc/couchdb-python/

*Please note: You might have to adjust the IP and hopefully the password in the GET request*

## send.py
Script to send signals for 433mhz power sockets from EASY HOME (ALDI) made for the Raspberry Pi.
The script can be used like this:
Turn socket chanel a on:
```
python send.py a_on
```
Turn the same socket off:
```
python send.py a_off
```

## analyse_signal.py
The script is able to record 433mhz signals and store them in files. Beside that the script can also do the following tasks:
+ Plot the raw signal to a digram
+ Record raw data to a file
+ Read recorded data
+ Show timing values for the signal

To use all parts of the script the following dependencies have to be installed:

+ https://github.com/jsonpickle/jsonpickle
+ https://matplotlib.org/users/installing.html

Below are some examples on how the script can be used:

### Show help
```
python analyse_signal.py --help
```
### Record a signal and store it in a file
```
python analyse_signal.py -rec -write data.json
```
*It is possible to change the time and input pin that is used for the operation above by setting -duration 2 -i_pin 22*

### Send a stored signal directly 
```
python analyse_signal.py -read data.json -fastsend
```
*Please note that this will create all data on the fly and will take some more time as using a trasnmit file created with -create, see below*

### Create a transmit file
```
python analyse_signal.py -create
```
This will guide you, it is also possible to call this directly with -read or -rec

### Send a transmit file
```
python analyse_signal.py -tranmit a_on.json
```
Send a transmit file, faster as -fastsend as the data is used from the file

Verbose printing can be activated by using -verbose
### Full example
```
python analyse_signal.py -rec -write m_on_r.json 
Starting recording in 2s, be ready
Starting...
Recording done
python analyse_signal.py -plot -read m_on_r.json 
python analyse_signal.py -create -read m_on_r.json 
Transmit file done
Path to save file:m_on.json
File created, use the -transmit option to send this file
python analyse_signal.py -transmit m_on.json -o_pin 27
```
+ record raw data to a file
+ plot recorded data to diagram
+ create a transmit file from the recorded data
+ send transmit file with pin 27




