#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint8_t anonymous_func(uint64_t x)
{
	uint8_t ret = 0;
	
	while (x) {
		++ret;
		x &= x - 1;
	};
	
	return ret;
}

int main(void)
{
	printf("the 1 bit in %d is %d.\n", 3, anonymous_func(3));
	return 0;
}
