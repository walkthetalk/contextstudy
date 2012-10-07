#include <stdio.h>
#include <stdlib.h>

void printA(void)
{
	char str[]="Hello";
	char*p=str;
	int n=100;

	printf("case A:\n");
	printf("sizeof(str)= %u\n", sizeof(str));
	printf("sizeof(p)= %u\n", sizeof(p));
	printf("sizeof(n)= %u\n", sizeof(n));
}

void printB(char str[100])
{
	printf("case B:\n");
	printf("sizeof(str)= %u\n", sizeof(str));
}

void printC(void)
{
	void * p = malloc(100);
	printf("case C:\n");
	printf("sizeof(p)= %u\n", sizeof(p));
	free(p);
}

int main(void)
{
	char str[100] = "";
	printA();
	printB(str);
	printC();
	return 0;
}
