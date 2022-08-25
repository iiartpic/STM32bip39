#include "Bitcoin.h"

String parsedMsg[2]; //parsedMsg[0] строковое представление выбранных номеров из питона \ parsedMsg[1] - энтропия

const size_t bufferSize = 255;
int arr[bufferSize]; // массив выбранных номеров из питона
int length_arr;

boolean arrayIncludeElement(int array[], int element) {
  for (int i = 0; i < length_arr; i++) {
      if (array[i] == element) {
          return true;
      }
    }
  return false;
}

void printAddresses(String mnemonic, String password = ""){
  // last time we used mnemonic, let's use xprv this time
  HDPrivateKey root(mnemonic, password);
  HDPrivateKey account = root.derive("m/44'/0'/0'");
  // print account and it's xpub
  Serial.println();
  Serial.print("Root: ");
  Serial.println(root);
  Serial.print("Account: ");
  Serial.println(account);
  Serial.print("Xpub: ");
  Serial.println(account.xpub());

  // this is out account xpub from previous part
  HDPublicKey xpub(account.xpub());
  HDPublicKey pub;

  for(int i=0; i<256; i++){
    if (arrayIncludeElement(arr, i)){
      String path = String("m/44'/0'/0'/0/")+i;
      Serial.print(path+"   ");
      pub = xpub.child(0).child(i);
      Serial.println(pub.address());
      //Serial.println("true");
    }
  }

}

void stringToArray(String sp){  
  int str_len = sp.length() + 1; 
  char str[str_len];
  sp.toCharArray(str, str_len);
  
//  const size_t bufferSize = 5;
//  int arr[bufferSize];
  
  char *p = strtok(str, ",");
  size_t index = 0;
  
  while (p != nullptr && index < bufferSize) {
    arr[index++] = atoi(p);
    p = strtok(NULL, ",");
  }
  length_arr = index;

  //for (size_t i = 0; i < index; i++)
  //  Serial.println(arr[i]);

}

void  stringPars(String Msg){
  int r = 0, t = 0;
  
  for (int i = 0; i < Msg.length(); i++) {
    //if (Msg[i] == ' ' || Msg[i] == ';'){
    if (Msg[i] == ';'){
      if (i - r > 1){
        parsedMsg[t] = Msg.substring(r, i);
        t++;
      }
      r = (i + 1);
    }
  }
  //for (int k = 0; k <= t; k++)
  //{
  //  Serial.println(parsedMsg[k]);
  //}
}


void bip39(String _pin){
  Serial.println();
  Serial.print("Entropy: ");
  Serial.println(_pin);
  Serial.println();
  String phrase = generateMnemonic(24, _pin);
  Serial.println(phrase);

  stringToArray(parsedMsg[0]);
  printAddresses(phrase);

}

void setup()
{
  Serial.begin(115200);
  while (!Serial) {}
    Serial.println("python -m serial.tools.list_ports | python -m serial.tools.miniterm <port_name>");
}

void loop(){
  if (Serial.available()) {
    String s = Serial.readStringUntil('\n');
    s.trim(); // strip off any leading/trailing space and \r \n
    if (s.length() > 0) {
      //parsed 2,4,7,9;12345;
      stringPars(s);
      bip39(parsedMsg[1]);  
    
      Serial.println("------------- END -------------");    
    }
  }

  delay(10);
}
