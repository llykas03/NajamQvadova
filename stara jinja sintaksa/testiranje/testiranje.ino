#include <WiFi.h>
#include "time.h"
#include "esp_sntp.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#define RED_PIN 14      // Pin za crvenu boju
#define GREEN_PIN 13    // Pin za zelenu boju
#define BLUE_PIN 12     // Pin za plavu boju
#define relejPin 23

const char *ntpServer1 = "pool.ntp.org";
const char *ntpServer2 = "time.nist.gov";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;

const char *time_zone = "CET-1CEST,M3.5.0,M10.5.0/3"; 

LiquidCrystal_I2C lcd(0x27, 16, 2);

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
  povezivanjeNaWifi("Cekic Network","0642832134m");

  //konfiguracija za tacno vreme i datum
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer1, ntpServer2);
}

void loop() {

   
  prikaziNaEkranu(tacnoVreme());
  kontrolisiRelej(1);
  delay(2000);
  prikaziNaEkranu(tacnoDatum()); 
  kontrolisiRelej(0);
  delay(2000); 

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
    strftime(buffer, sizeof(buffer), "%a,%d,%b %Y", &timeinfo);

    return String(buffer);  // Vraća samo datum i godinu kao string
}
String tacnoVreme() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        return "Nema dostupnog vremena";
    }

    char buffer[50];
    // Formatiramo vreme kao "12:45:30"
    strftime(buffer, sizeof(buffer), "%H:%M:%S", &timeinfo);

    return String(buffer);  // Vraća samo vreme kao string
}
void kontrolisiRelej(int stanje) {
  if (stanje == 1) {
    setColorLED(3);
    digitalWrite(relejPin, HIGH);  // Uključi relej (visok signal)
  } else if (stanje == 0) {
    setColorLED(1);
    digitalWrite(relejPin, LOW);   // Isključi relej (niski signal)
  }
}
