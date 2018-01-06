
#define input_pin 2
#define interupt  0
#define start_time 740
#define stateLength 65535
#define start_offset 0
#define min_startBytes 4

volatile boolean start = false;
volatile unsigned int stateHigh[120]; 
volatile unsigned int stateLow[120];
volatile unsigned int counter = 0;
volatile int startCounter = 0;


void setup() {
  // Set pin to input and register interrupt
  pinMode(input_pin,INPUT);
  attachInterrupt(interupt, change, CHANGE);
  Serial.begin(115200);
  Serial.println("Go");
}

void change()
{
  static long high,low;
  long result = 0;
  int state = digitalRead(input_pin);
  if(state == HIGH)
  {
    high = micros();
    result = safeValue(high - low);
    if(start)
    {
      //Add new time to low
      stateLow[counter]= result;
      counter++;//Move
      if(counter >= 120)
      {
        counter = 0; //reset
      }
    }
    else
    {
      result -= start_time;
      if(abs(result) <= start_offset)
      {
        startCounter++;
      }
      if(startCounter >= min_startBytes)
      {
        start = true;
        startCounter= 0;
      }
    }
  }
  else
  {
    low = micros();
    result = safeValue(low - high);
    if(start)
    {
      stateHigh[counter]= result;
    }
    else
    {
      result -= start_time;
      if(abs(result) <= start_offset)
      {
        startCounter++;
      }
      if(startCounter >= min_startBytes)
      {
        start = true;
        startCounter= 0;
      }
    }
  }
}

unsigned int safeValue(long value)
{
     if(value > stateLength) 
     {
       value = stateLength;
     }
     return value;
}
  
void encode()
{
    //Try to find 1 and 0 in signal and print
}

void loop() {
  // put your main code here, to run repeatedly:
  if(start)
  {
    if(counter >= 80)
    {
        Serial.print("Start found at ");
        Serial.println(millis());
        Serial.println("5 bytes found");
        noInterrupts();
        //Reset
        counter = 0;
        start = false;
        //Print
        for(int i=0; i<80;++i)
        {
          Serial.print(stateHigh[i]);
          Serial.print(",");
          Serial.println(stateLow[i]);
        }
        interrupts();
    }
  }

}
