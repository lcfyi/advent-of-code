#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* itoa(int val, int length) {
	char *buffer = malloc(length + 1);
	int i = length;
    buffer[length] = 0;
    while (val) {
        buffer[--i] = "0123456789"[val % 10];
        val /= 10;
    }
    return buffer;
}

int verify_number(int num) {
    char * buffer = itoa(num, 6);
    // Verify it's monotonic
    for (int i = 1; i < 6; i++) {
        if (buffer[i - 1] > buffer[i]) {
            return 0;
        }
    }

    // Verify that there's no double
    int count = 1;
    for (int i = 1; i < 6; i++) {
        if (buffer[i - 1] == buffer[i]) {
            count++;
        } else {
            if (count == 2) {
                return 1;
            }
            count = 1;
        }
    }
    if (count == 2) {
        return 1;
    } else {
        return 0;
    }
}

int main(void) {
    int start = 245318;
    int end = 765747;

    int count = 0;

    for (int i = start; i <= end; i++) {
        if (verify_number(i)) {
            count++;
        }
    }

    printf("%d\n", count);

    return 0;
}