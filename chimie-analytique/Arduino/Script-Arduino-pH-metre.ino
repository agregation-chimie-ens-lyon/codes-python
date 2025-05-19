// Script permettant de simuler le fonctionnement d'un pH-mètre :

int pinpH = A0; // broche réliée à l'électrode de verre
float UpH; // tension de l'électrode de verre
float UpH4; // tension pour pH = 4
float UpH7; // tension pour pH = 7
float slope; // pente b de U = a + b * pH
float intercept; // ordonnée à l'origine a de U = a + b * pH
float rawSignal; // tension brute non moyennée
float alpha = 0.05; // pour calculer une moyenne exponentielle
float pH; // calcul du pH

int TempsEntreAffichage = 1000;
float TempsAffichageSuivant;

// void setup pour programmer les différents programmes, exécuté une seule fois :

void setup() {
 Serial.begin(9600);
 pinMode(pinpH, INPUT);
 TempsAffichageSuivant = millis() + TempsEntreAffichage;
}

// boucle loop utilisée :

void loop() {
 rawSignal = analogRead(pinpH); // lecture tension brute
 UpH = alpha*rawSignal + (1-alpha)* UpH; // moyennage pour une meilleure stabilité
 // Écriture phrase réponse :

 if ( millis() > TempsAffichageSuivant ) {
   Serial.print("Tension brute ");
   Serial.print( UpH);
   Serial.print(" > UpH = ");
   Serial.println(String((UpH-intercept)/slope,3));

   if (Serial.available()){
     Serial.println("Hello"); // vérification fonctionnement clavier
     String init = Serial.readString();
     init.trim(); // mise en page phrase réponse
     if (init == "7"){
       Serial.println("Mémorisation de la valeur UpH7");
       UpH7 = UpH;
     }else if (init == "4"){
       Serial.println("Mémorisation de la valeur de UpH4");
       UpH4 = UpH; //permet de rentrer et mémoriser les valeurs des solutions étalons
     }
     slope = (UpH7-UpH4)/(7.-4.);
     intercept = UpH4 - slope*4.; // relation tension pH grâce à l'étalonnage
   }
   TempsAffichageSuivant = TempsAffichageSuivant + TempsEntreAffichage; // prise de point
 }
}
