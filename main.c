#include <stdio.h>
#include <string.h>

int main( int argc, char *argv[] )
{
const char wav_check[5] = ".wav";
const char txt_check[5] = ".txt";
char *wav_ret;
char *txt_ret;
wav_ret = strstr(argv[1], wav_check);
txt_ret = strstr(argv[2], txt_check);

   if( argc == 3 ) {
        if ((wav_ret = ".wav") && (txt_ret = ".txt")) {
            printf("Continue\n");
        
            
            
            
            
            
            
        }
        else {
            printf("ERROR: Please enter only .wav and or .txt files");
        }
   }
   else {
      printf("ERROR: insufficient arguments. Enter main.c 'example_file.wav' 'example_data.txt'\n");
   }
   
   return (0);
}