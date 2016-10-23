#include<stdio.h>

/*
 * This file takes a csv and swaps it to newline delimited.
 * Hopefully this will make large id files easier to use.
 */
int main(int argc, char** argv){

  char* nameIn = argv[1];
  char* nameOut = argv[2];

  FILE* inFile = fopen(nameIn, "r");
  printf("%d %s %s\n", argc, nameIn, nameOut);
  FILE* outFile = fopen(nameOut, "w");

  char charIn = 'q';

  while((charIn = getc(inFile)) != EOF){
    if(charIn == ','){
      putc('\n', outFile);
    }
    else{
      putc(charIn, outFile);
    }
  }
  fclose(inFile);
  fclose(outFile);
  return 0;
}
