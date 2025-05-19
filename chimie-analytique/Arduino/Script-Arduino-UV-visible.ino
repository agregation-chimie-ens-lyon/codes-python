// Script permettant de simuler le fonctionnement d'un spectro UV-vis :

int PinLED = 8; // Voie reliant la lED
int PinPhotoDiode = A0; // Voie reliant la photodiode

float Son;
float Soff;
int Tstab = 10;
float Smesure; // Représente l'intensité résultante

float S0 = 500.0; //Signal blanc (valeur arbitraire)
float alpha = 0.05; //permet de calculer une moyenne exponentielle
float A; //Absorbance

int TempsEntreAffichage = 1000;
float TempsAffichageSuivant;

// Void setup pour faire fonctionner les fonctions et initialiser la carte sur une seule boucle

void setup() {
 Serial.begin(9600);
 pinMode(PinLED, OUTPUT);
 pinMode(PinPhotoDiode, INPUT);

 TempsAffichageSuivant = millis() + TempsEntreAffichage;
}

// Boucle infinie contenant la fonction désirée

void loop() {

 digitalWrite (PinLED, HIGH); delay(Tstab);
 Son = analogRead(PinPhotoDiode); // lecture valeur photodiode

 digitalWrite(PinLED, LOW); delay(Tstab);
 Soff = analogRead(PinPhotoDiode); // lecture valeur photodiode

 Smesure = alpha * (Son-Soff) + (1-alpha) * Smesure; // moyennage de l'intensité

 if (millis() > TempsAffichageSuivant) {
   Serial.print(Son);Serial.print(" ");
   Serial.print(Soff); Serial.print(" > Abs =");
   Serial.println(log10(S0/Smesure),3); // écriture de la phrase réponse

   if (Serial.available()) {
     Serial.println("Hello"); // vérifier que le terminal marche
     String init = Serial.readString(); //Lecture jusqu'à l'arrêt
     init.trim(); // mise en page de la réponse
     if (init == "0") {
       Serial.println("Mémorisation de la valeur de S0"); //faire le blanc et vérifier que c'est fait
       S0 = Smesure;
     }
   }
   TempsAffichageSuivant = TempsAffichageSuivant + TempsEntreAffichage; //prise de point
 }
}





