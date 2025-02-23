#include <WiFi.h>
#include "time.h"
#include "esp_sntp.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#define RED_PIN 14      // Pin za crvenu boju
#define GREEN_PIN 13    // Pin za zelenu boju
#define BLUE_PIN 12     // Pin za plavu boju
#define relejPin 23

const char *ntpServer1 = "pool.ntp.org";
const char *ntpServer2 = "time.nist.gov";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;
LiquidCrystal_I2C lcd(0x27, 16, 2);


//default parametri
//url racunara odnosno ip adresa racunara na kom se pokrece python kod
String serverUrl = "http://160.99.40.134:5000/";
//wifi lokalna mrezna na kojoj su povezani i esp32 i racunar
const String WifiName = "SamsungAppsLab";
const String WifiPassword = "Samsung#2010";
//vremenska zona
const char *time_zone = "CET-1CEST,M3.5.0,M10.5.0/3"; 


void setup() {
  Serial.begin(115200);
  //relej config
  pinMode(relejPin, OUTPUT);  // Postavljanje releja kao izlaz
  digitalWrite(relejPin, LOW);
  //definisanje pinova za rgb diodu
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  //definisanje lcd ekrana
  lcd.begin();               
  lcd.backlight();

//metoda za povezivanje na wifi
  povezivanjeNaWifi(WifiName,WifiPassword);

  //konfiguracija za tacno vreme i datum
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer1, ntpServer2);
  
}

void loop() {
  //kvad nije iznajmljen sija crveno svetlo relej je otvoren
 setColorLED(1);
 kontrolisiRelej(0);
 prikaziNaEkranu("hello world");

 int wordCount = 0;
 String kvad =  getServerMessage("iznajmiKvad");
 String* NizKvad = splitStringToWords(kvad, wordCount);

int stop = iznajmljivanje(NizKvad);

  if(stop == 0){
    prikaziNaEkranu("admin je ugasio vozilo");
  }
 
  delay(5000);  
}

String getServerMessage(String route) {
    
    while (true) {  // Beskonačna petlja dok ne stigne validna poruka
        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;
            String fullUrl = String(serverUrl) + route;

            http.begin(fullUrl);
            int httpResponseCode = http.GET();

            if (httpResponseCode == 200) {
                String response = http.getString();
                http.end();

              StaticJsonDocument<200> doc;
              DeserializationError error = deserializeJson(doc, response);

              if (!error) {
                String message = doc["message"].as<String>();
                response = message;
              }  
                
                if (response != "" && response != "nema poruke") {  
                    return response;  // Ako je poruka validna, prekini petlju i vrati je
                }
            } else if (httpResponseCode == 204) {
                Serial.println("nema poruke");
            }
            http.end();
        } else {
            Serial.println("Wi-Fi nije povezan!");
        }
        
        delay(1000); // Kratak pauza pre sledećeg pokušaja
    }
}
void sendMessageToServer(String message, String route) {
  // Provera da li je ESP32 povezan na WiFi
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Povezivanje sa serverom koristeći URL i rutu
    String fullUrl = serverUrl + route;
    http.begin(fullUrl);  

    // Postavljanje Content-Type zaglavlja
    http.addHeader("Content-Type", "application/json");

    // Kreiranje JSON payload-a sa porukom
    String jsonData = "{\"message\": \"" + message + "\"}";

    // Slanje POST zahteva
    int httpResponseCode = http.POST(jsonData);

    // Provera odgovora od servera
    if (httpResponseCode > 0) {
      String response = http.getString();  // Čitanje odgovora od servera
      Serial.println("Odgovor servera: " + response);
    } else {
      Serial.println("Greška pri slanju zahteva: " + String(httpResponseCode));
    }

    // Zatvaranje HTTP konekcije
    http.end();
  } else {
    Serial.println("Wi-Fi nije povezan!");
  }
}
void povezivanjeNaWifi(String ssid,String password){

  prikaziNaEkranu("wifi konfig");
  WiFi.begin(ssid, password);
  esp_sntp_servermode_dhcp(1);  // (optional)

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    prikaziNaEkranu("povezivanje");
  }
  prikaziNaEkranu("povezano");
  
}
void prikaziNaEkranu(String poruka) {
    lcd.clear();  // Očisti ekran pre prikazivanja nove poruke

    int duzinaPoruke = poruka.length();

    // Ako je poruka kraća ili jednaka 16 karaktera, centriraj na prvi red
    if (duzinaPoruke <= 16) {
        // Računanje pozicije za centriranje na prvom redu
        int pozicijaX = (16 - duzinaPoruke) / 2;
        lcd.setCursor(pozicijaX, 0);  // Postavi kursor na prvi red, odgovarajući položaj
        lcd.print(poruka);  // Ispisivanje poruke na prvi red
    }
    // Ako je poruka duža od 16 karaktera, podeli je na dva dela
    else {
        String prviRed = poruka.substring(0, 16);    // Prvih 16 karaktera za prvi red
        String drugiRed = poruka.substring(16);      // Ostatak za drugi red

        // Računanje pozicije za centriranje na prvom redu
        int pozicijaX1 = (16 - prviRed.length()) / 2;
        lcd.setCursor(pozicijaX1, 0);  // Postavi kursor na prvi red
        lcd.print(prviRed);   // Ispisivanje prvih 16 karaktera na prvom redu

        // Računanje pozicije za centriranje na drugom redu
        int pozicijaX2 = (16 - drugiRed.length()) / 2;
        lcd.setCursor(pozicijaX2, 1);  // Postavi kursor na drugi red
        lcd.print(drugiRed);  // Ispisivanje ostatka poruke na drugom redu
    }
}
void setColorLED(int boja) {
    analogWrite(RED_PIN, 0);
    analogWrite(GREEN_PIN, 0);
    analogWrite(BLUE_PIN, 0);
     switch (boja) {
        case 1:
            analogWrite(RED_PIN, 255);
            analogWrite(BLUE_PIN, 0);
            analogWrite(GREEN_PIN, 0);
            
            break;
    
        case 2:
            analogWrite(RED_PIN, 255);
            analogWrite(GREEN_PIN, 255);
            analogWrite(BLUE_PIN, 0);
            break;
    
        case 3:
            analogWrite(GREEN_PIN, 255);
            analogWrite(RED_PIN, 0);
            analogWrite(BLUE_PIN, 0);
            break;
    
        case 4:
            analogWrite(BLUE_PIN, 255);
            analogWrite(GREEN_PIN, 0);
            analogWrite(RED_PIN, 0);
            break;
    
        default:
            // Opcionalno, resetujte boje ili unesite dodatnu logiku za nepoznate boje
            analogWrite(RED_PIN, 0);
            analogWrite(GREEN_PIN, 0);
            analogWrite(BLUE_PIN, 0);
            break;
    }

}
String tacnoDatum() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        return "Nema dostupnog vremena";
    }

    char buffer[50];
    // Formatiramo datum kao "mon, 14, nov 2024" sa skraćenicom za mesec
    strftime(buffer, sizeof(buffer), "%d.%m.%Y", &timeinfo);

    return String(buffer);  // Vraća samo datum i godinu kao string
}
String tacnoVreme() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        return "Nema dostupnog vremena";
    }

    char buffer[50];
    // Formatiramo vreme kao "12:45:30"
    strftime(buffer, sizeof(buffer), "%H:%M", &timeinfo);

    return String(buffer);  // Vraća samo vreme kao string
}
void kontrolisiRelej(int stanje) {
  if (stanje == 1) {
    digitalWrite(relejPin, HIGH);  // Uključi relej (visok signal)
  } else if (stanje == 0) {
    digitalWrite(relejPin, LOW);   // Isključi relej (niski signal)
  }
}
int iznajmljivanje(String* niz){
 
  int hours = niz[2].toInt();
  String idKorisnika = niz[0];
  String idKvada = niz[1];

  setColorLED(3);
  prikaziNaEkranu("Kvad Iznajmljen Na "+String(hours)+" Sat");
  delay(5000);
  prikaziNaEkranu("User ID:"+idKorisnika);
  delay(5000);
  kontrolisiRelej(1);
  int totalMinutes = hours * 60;

    while (totalMinutes >= 0) {

        int hh = totalMinutes / 60;
        int mm = totalMinutes % 60;

        // Kreiranje stringa u formatu HH:MM
        String timeLeft = (hh < 10 ? "0" : "") + String(hh) + ":" + 
                          (mm < 10 ? "0" : "") + String(mm);

        
        prikaziNaEkranu("Preostalo vreme:"+timeLeft); // Štampanje
        
        if(proveraZaustavljanja("stopVozilo")){
          sendMessageToServer(idKorisnika,"isteklovreme");
          return 0;
          
        };
        
        delay(40000); // Sačekaj 1 minut

      prikaziNaEkranu("Vreme:"+tacnoVreme());
      delay(10000);
      prikaziNaEkranu("Datum:"+tacnoDatum());
      delay(10000);

      if(totalMinutes==10){
        prikaziNaEkranu("imate jos 10     minuta");
        setColorLED(2);
        delay(10000);
      }

        totalMinutes--;
    }
    setColorLED(1);
    kontrolisiRelej(0);
    prikaziNaEkranu("vreme je        isteklo");
    sendMessageToServer(idKorisnika,"isteklovreme");
    return 1;


}
String* splitStringToWords(String inputString, int &wordCount) {
  // Maksimalni broj reči koje ćemo podržati, možeš promeniti po potrebi
  static String words[20];  
  wordCount = 0;
  
  int startIndex = 0;
  
  for (int i = 0; i < inputString.length(); i++) {
    if (inputString.charAt(i) == ',') {  // Kada naiđeš na zarez
      // Izdvaja podstring između prethodnog indeksa i trenutnog indeksa
      String word = inputString.substring(startIndex, i);
      word.trim();  // Ukloni razmake sa početka i kraja reči
      if (word.length() > 0) {  // Ako reč nije prazna
        words[wordCount++] = word;  // Dodaj reč u niz
      }
      
      startIndex = i + 1;  // Postavi početni indeks na poziciju nakon zareza
    }
  }
  
  // Poslednja reč
  String word = inputString.substring(startIndex);
  word.trim();  // Ukloni razmake sa početka i kraja
  if (word.length() > 0) {  // Ako reč nije prazna
    words[wordCount++] = word;  // Dodaj reč u niz
  }
  
  return words;  // Vraća niz reči
}
bool proveraZaustavljanja(String ruta){

    HTTPClient http;
    String fullUrl = String(serverUrl) + ruta;
    http.begin(fullUrl);

    int httpResponseCode = http.GET();
    bool shouldStop = false;  // Podrazumevano vraćamo false

    if (httpResponseCode == 200) {
        String response = http.getString();
        http.end();

        StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, response);

            if (!error) {
                String message = doc["message"].as<String>();

                // Provera poruke
                if (message == "stop") {
                    Serial.println("STOP! Vozilo mora stati!");
                    shouldStop = true;
                } else {
                    Serial.println("Primljena poruka: " + message);
                    shouldStop = false;
                }
            } else {
                Serial.println("Greška pri parsiranju JSON-a!");
            }
        
    } else if (httpResponseCode == 204) {
        Serial.println("Nema poruke od servera");
        return false;
    } else {
        Serial.println("HTTP greška: " + String(httpResponseCode));
    }

    http.end();
    return shouldStop;
}
