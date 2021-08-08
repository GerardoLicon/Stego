#include <stdio.h>

int main( int argc, char *argv[] )  {

   if( argc == 2 ) {
      printf("Continue\n");
      
      
   }
   else if( argc > 2 ) {
      printf("ERROR: insufficient arguments. Enter main.c 'file.wav' 'target_data.txt'\n");
   }
   else {
      printf("ERROR: insufficient arguments. Enter main.c 'file.wav' 'target_data.txt'\n");
   }
}