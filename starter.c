#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    FILE *file;


    file = fopen("input.txt", "r");

    // Read entire file
    // char *data = 0;
    // long length = 0;
    // if (file) {
    //     fseek(file, 0, SEEK_END);
    //     length = ftell(file);
    //     fseek(file, 0, SEEK_SET);
    //     data = malloc(length);

    //     if (data) {
    //         fread(data, 1, length, file);
    //     }

    //     fclose(file);
    // }

    // Read lines
    // char **data = malloc(1);
    // long length = 0;

    // if (file) {
    //     int read_bytes;
    //     size_t len = 0;
    //     char *line;
    //     while (getline(&data[length], &len, file) != -1) {
    //         data = realloc(data, 1);
    //         length++;
    //     }
    //     fclose(file);
    // }

    return 0;
}