#include <Redis.h>
#include <RedisInternal.h>
#include <ArduinoJson.h>
#include <MQ2.h>
// #include <Preferences.h>
#include <WiFi.h>
#include <Esp32WifiManager.h>
#include <ctime>
#include <iostream>

#define RELAY1 9

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by unix time_t as ten ascii digits
#define TIME_HEADER  255   // Header tag for serial time sync message
#define DELAYERREUR 25

int number = 0;
int sensorMqPin = 32;
int sensorTemperatureAnalogPin = 25;
int detecteurEauElectriquePin=39;
int detecteurEauTraitementPin=34;
int detecteurMouvementPin=36;
int detecteurPanneElectriquePinIn=37;
int systemeArrosagePin1 = 13;
int systemeArrosagePin2 = 13;
int systemeArrosagePin3 = 13;
int systemeArrosagePin4 = 13;
bool systemeDetectionPosition=false;
bool activationSystemeArrosage=false;
int debug = 0;
int lpg, co, smoke;

const char* ssid     = "Personnel2020";
const char* password = "lapechealatruite2019";
#define MAX_BACKOFF 300000 // 5 minutes


// pour établir la date et l heure du esp32 selon Montreal
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = -18000;
const int   daylightOffset_sec = 3600;

String requete="";

unsigned long previousMillis = 0;        // will store last time LED was updated
unsigned long interval = 1300;  


struct DETECTEUR {
  float Prop;
  float Co;
  float Fumee;
  float Mouvement;
  float EauElectrique;
  float EauTraitement;
  float PanneElectrique;
  float Arrosage;
  float Temperature;

}  Temp;

#define REDIS_ADDR "192.168.1.125"
#define REDIS_PORT 6379
#define REDIS_PASSWORD ""



MQ2 mq2(sensorMqPin);
WiFiClient redisConn;

void setup()
{
  Serial.begin(115200);
  WiFiClient redisConn;
  
  // configure pour la date et l'heure de Montreal avec un ntp serveur
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

 
  mq2.begin();
  delay(10);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // WiFiClient redisConn;
  if (!redisConn.connect(REDIS_ADDR, REDIS_PORT))
  {
    Serial.println("Failed to connect to the Redis server!");
    
  }


    auto backoffCounter = -1;
    auto resetBackoffCounter = [&]() { backoffCounter = 0; };

    resetBackoffCounter();
    while (subscriberLoop(resetBackoffCounter))
    {
        auto curDelay = min((1000 * (int)pow(2, backoffCounter)), MAX_BACKOFF);

        if (curDelay != MAX_BACKOFF)
        {
            ++backoffCounter;
        }

        Serial.printf("Waiting %ds to reconnect...\n", curDelay / 1000);
        delay(curDelay);
    }

    Serial.printf("Done!\n");
 
  setPinMode(sensorTemperatureAnalogPin, INPUT);
  setPinMode(detecteurEauElectriquePin, INPUT);
  setPinMode(detecteurEauTraitementPin, INPUT);
  setPinMode(detecteurMouvementPin, INPUT);
  setPinMode(detecteurPanneElectriquePinIn, INPUT);
    
  // pour le relai du systeme arrosage
  setPinMode(systemeArrosagePin1, OUTPUT);
  digitalWrite(systemeArrosagePin1, LOW);

}

void msgCallback(Redis *redisInst, String channel, String msg) {
  Serial.printf("Message on channel '%s': \"%s\"\n", channel.c_str(), msg.c_str());

  if (channel == "ctrl-close")
  {
    Serial.println("Got message on ctrl-close: ending!");
    redisInst->stopSubscribing();
  }
  else if (channel == "ctrl-add")
  {
    Serial.printf("Adding subscription to channel '%s'\n", msg.c_str());

    if (!redisInst->subscribe(msg.c_str()))
    {
      Serial.println("Failed to add subscription!");
    }
  }
  else if (channel == "ctrl-rm")
  {
    Serial.printf("Removing subscription to channel '%s'\n", msg.c_str());

    if (!redisInst->unsubscribe(msg.c_str()))
    {
      Serial.println("Failed to remove subscription!");
    }
  }
}

void errorCallback(Redis *redisInst, RedisMessageError err) {
  (void)redisInst; // quiet compiler warning about unused parameter
  Serial.printf("Subscription error! '%d'\n", err);
}

// returning 'true' indicates the failure was retryable; false is fatal
bool subscriberLoop(std::function<void(void)> resetBackoffCounter)
{

  if (!redisConn.connect(REDIS_ADDR, REDIS_PORT))
  {
    Serial.println("Failed to connect to the Redis server!");
    return true;
  }


  Redis redis(redisConn);
  
  Serial.println("passe 1 ");
  redis.subscribe("publishArduinoRequete");
  Serial.println("passe 2 ");

  redis.psubscribe("ctrl-*");

  Serial.println("Listening...");
  resetBackoffCounter();
  Serial.println("passe 2 ");
  auto subRv = redis.startSubscribingNonBlocking(msgCallback, loop, errorCallback);
  requete=subRv;
  Serial.println("passe 5 ");
  // redisConn.stop();
  Serial.printf("Connection closed! (%d)\n", requete);
  return subRv == RedisSubscribeServerDisconnected; // server disconnect is retryable, everything else is fatal
};


void loop() {
  Serial.printf("Requete \n ", requete);
  
  // relai soit en position ouvert
  if (requete=="Gicleur_1_ON"){
    setPinEsp32(systemeArrosagePin1, HIGH);
  }
  
  // relai soit en position fermé
  if (requete=="Gicleur_1_OFF"){
    setPinEsp32(systemeArrosagePin1, LOW);
  }

  // relai soit en position ouvert
  if (requete=="Gicleur_2_ON"){
    setPinEsp32(systemeArrosagePin2, HIGH);
  }
  
  // relai soit en position fermé
  if (requete=="Gicleur_2_OFF"){
    setPinEsp32(systemeArrosagePin2, LOW);
  }

  // relai soit en position ouvert
  if (requete=="Gicleur_3_ON"){
    setPinEsp32(systemeArrosagePin3, HIGH);
  }
  
  // relai soit en position fermé
  if (requete=="Gicleur_3_OFF"){
    setPinEsp32(systemeArrosagePin3, LOW);
  }

  // relai soit en position ouvert
  if (requete=="Gicleur_4_ON"){
    setPinEsp32(systemeArrosagePin4, HIGH);
  }
  
  // relai soit en position fermé
  if (requete=="Gicleur_4_OFF"){
    setPinEsp32(systemeArrosagePin4, LOW);
  }
  
  if (requete=="97"){
    debug=1;
  }
  if (requete=="98"){
    debug=0;
  }

/*
 Serial.print (" Interval pour assigner aux variables ");
 Serial.print (" millis() = ");
 Serial.print (millis());
 Serial.print (" previousMillis = ");
 Serial.print (previousMillis);
 Serial.print (" inteval = ");
 Serial.println(interval);
 */
 if (millis() - previousMillis > interval) {
    Serial.print("Valeur : ");
   
    assigneValeursAuxVariables();
  }  
  
  previousMillis += interval;

  // setPinEsp32(systemeArrosagePin, HIGH);
  delay(25);
  // setPinEsp32(systemeArrosagePin, LOW);
  requete="";
}

String getCurrentTime()
{
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");

  }
  
  char buffer[256];

  strftime(buffer, sizeof(buffer), "%a %b %d %H:%M:%S %Y", &timeinfo);
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  return buffer;
}


float getPinStatut(int pinNo){
  float resultat;
  
    resultat = analogRead(pinNo); 
    if (resultat > 4000){
      resultat = 0;
    }else{
      resultat = 1;
    }
    return resultat;
  }


// statut du gicleur d arrosage
float getStatutOutputPin(int pin){
  int resultat=0;
  int resultatFloat=0.0;
  
  resultatFloat = digitalRead(pin);
  
  if (resultatFloat == 0){
    resultatFloat=1.0;
  }else {resultatFloat=0.0;}
  
  return resultatFloat;
  
}

void setPinMode(int pinNo, int modeInputOutput){
  pinMode(pinNo, modeInputOutput);
}

void setPinEsp32(int pinNo, bool valeur){

  if (valeur==true){
    digitalWrite(pinNo, HIGH);
  }
  else{
    digitalWrite(pinNo, LOW);   
  }
  
 
}

/*
float Temperature(int sensorTemperatureAnalogPin){
  //getting the voltage reading from the temperature sensor
   int reading = analogRead(sensorTemperatureAnalogPin);  
   
   //Serial.print(reading); Serial.println(" volts 1");
   // converting that reading to voltage, for 3.3v arduino use 3.3
   float voltage = reading  * 5.0;
   voltage /= 1024.0; 

   Serial.print("Voltage : ");
   Serial.println(reading);
   
   // print out the voltage
   //Serial.print(voltage); Serial.println(" volts 2");
   
   // now print out the temperature
   float temperatureC = (voltage - 0.5) * 100 ;  //converting from 10 mv per degree wit 500 mV offset
                                                 //to degrees ((voltage - 500mV) times 100)
  // Serial.print(temperatureC); Serial.println(" degrees C");
   
   // now convert to Fahrenheit
   float temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
   //Serial.print(temperatureF); Serial.println(" degrees F");++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


   if (debug==1){
    Serial.print("Detecteur de temperature reading : ");
    Serial.print(reading);
    Serial.print("   ");
    Serial.print("voltage : ");
    Serial.print(voltage);
    Serial.print("   ");
    Serial.print("temperature : ");
    Serial.print(temperatureC);
    Serial.println();   
   }
   
   return temperatureC;
}

*/

void assigneValeursAuxVariables(){
    DynamicJsonDocument doc(250);
    char output[250];
    
    Temp.Mouvement=getPinStatut(detecteurMouvementPin);
    Temp.EauTraitement=getPinStatut(detecteurEauTraitementPin);
    Temp.EauElectrique=getPinStatut(detecteurEauElectriquePin);
    Temp.PanneElectrique= getPinStatut(detecteurPanneElectriquePinIn);
    Temp.Arrosage=getStatutOutputPin(systemeArrosagePin4);
    Temp.Temperature=0;

    
    doc["DateHeure"] = getCurrentTime();
    if (mq2.readCO() > 1000){
      doc["Prop"]=0;
    }else{doc["Prop"]=1000;}
    if (mq2.readCO() > 1000){
      doc["CO"]=0;
    }else{doc["CO"]=1000;}
    
    if (mq2.readSmoke() > 1000){
      doc["Fumee"]=0;
    }else{doc["Fumee"]=1000;}
    
    doc["Temperature"]=Temp.Temperature;
    doc["Mouvement"]= Temp.Mouvement;
    doc["EauElectrique"] = Temp.EauElectrique;
    doc["EauTraitement"] = Temp.EauTraitement;
    doc["PanneElectrique"] = Temp.PanneElectrique;
    doc["Arrosage"] = Temp.Arrosage; 

  
    WiFiClient redisConn1;
      if (!redisConn1.connect(REDIS_ADDR, REDIS_PORT))
      {
        Serial.println("Failed to connect to the Redis server!");
      }

    Redis redis1(redisConn1);
    
    Serial.println("passe 5 ");
    serializeJson(doc, output);
    Serial.println("passe 6 ");    
    redis1.publish("InterfaceArduinoDetecteurs", output);
    Serial.println("passe 7 ");
    // Serial.println(output);
    
    delay(200);
   
   
  if (debug==1){
    
    Serial.print(" PanneElectrique ");Serial.print(Temp.PanneElectrique);Serial.println();
    Serial.print(" Co ");Serial.print(Temp.Co);Serial.println();
    Serial.print(" Fumee ");Serial.print(Temp.Fumee);Serial.println();
    Serial.print(" Temperature ");Serial.print(Temp.Temperature);Serial.println();    
    Serial.print(" Mouvement ");Serial.print(Temp.Mouvement);Serial.println();
    Serial.print(" EauElectrique ");Serial.print(Temp.EauElectrique);Serial.println();
    Serial.print(" EauTraitement ");Serial.print(Temp.EauTraitement);Serial.println(); 
    Serial.print(" Arrosage ");Serial.print(Temp.Arrosage);Serial.println();
    Serial.print(" Code envoye page web ");Serial.print(requete);Serial.println(); 
  }
    
}



void serialEvent() {
  
   // Serial.println(" valeur de la requete 1" + requete);
    requete = (String)Serial.read();
    // add it to the inputString:
    
    delay(50);
   // serializeJson(doc, Serial);
    //Serial.println(" valeur de la requetec 2" + requete);
    
}
