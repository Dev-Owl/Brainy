
#define input_pin 2
#define interupt  0
#define start_time 740
#define stateLength 65535
#define start_offset 50
#define min_startBytes 4
#define pulseRange 250 
#define pulseOffset 100
#define checkLength 80
#define DEBUG  0
#define maxdata 120

volatile boolean start = false;
volatile unsigned int stateHigh[maxdata]; 
volatile unsigned int stateLow[maxdata];
volatile unsigned int counter = 0;
volatile int startCounter = 0;


void setup() {
  // Set pin to input and register interrupt
  pinMode(input_pin,INPUT);
  attachInterrupt(interupt, change, CHANGE);
  Serial.begin(115200);
  #if DEBUG == 1
  Serial.println("Go");
  #endif
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
      if(counter >= maxdata)
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
      else{
        startCounter =0;
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
      else{
        startCounter =0;
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
    boolean highLong = false;
    boolean lowLong  = false;
    int rhigh = 0;
    int rlow  = 0;
    int maxPulse = pulseRange*2+pulseOffset; 
    Serial.println();
    //Try to find 1 and 0 in signal and print
    for(int i=0; i<checkLength;++i)
    {
        
        if(stateHigh[i] > 32767)
          continue;
        if(stateLow[i] > 32767)
          continue;
        rhigh = stateHigh[i];
        rlow  = stateLow[i];
        if(rhigh <= pulseOffset)
          continue;
        if(rlow <= pulseOffset)  
          continue;
        if(rlow > maxPulse || rhigh > maxPulse)
          continue;
        rhigh -= pulseRange;
        rhigh = abs(rhigh);
        rlow  -= pulseRange;
        rlow = abs(rlow);
        
        if(rhigh <= pulseOffset)
        {
          highLong = false;
        }
        else
        {
          rhigh -= pulseRange;
          rhigh = abs(rhigh);
          if(rhigh <= pulseOffset)
          {
            highLong = true;
          }
          else
          {
            continue;
          }
        }
        if(rlow <= pulseOffset)
        {
          lowLong = false;
        }
        else
        {
          rlow -= pulseRange;
          rlow = abs(rlow);
          if(rlow <= pulseOffset)
          {
            lowLong = true;
          }
          else
          {
            continue;
          }
        }
        //if here the signal was in the range
        if(!highLong && lowLong)
        {
          Serial.print("0");
        }
        else
        {
          Serial.print("1");
        }
        
    }
    Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(start)
  {
    if(counter >= checkLength)
    {
        #if DEBUG == 1
        Serial.print("Start found at ");
        Serial.println(millis());
        Serial.println("5 bytes found");
        #endif
        noInterrupts();
        //Reset
        counter = 0;
        start = false;
        #if DEBUG == 1
        //Print
        for(int i=0; i<checkLength;++i)
        {
          Serial.print(stateHigh[i]);
          Serial.print(",");
          Serial.println(stateLow[i]);
        }
        #endif
        encode();
        interrupts();
    }
  }

}
