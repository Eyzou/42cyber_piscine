#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void no(void)
{
    printf("Nope.\n");
    exit(1);
}

int main(void)
{
    char input[64];
    char result_buffer[9];
    char ascii_buffer[4];

    printf("Please enter key: ");
    if (scanf("%63s",input) != 1)
        no();

    if (input[0] != '0' || input[1] != '0')
        no();

    fflush(stdout);

    memset(result_buffer,0, sizeof(result_buffer));
    result_buffer[0] ='d';

    unsigned int i = 2;
    unsigned int j = 1;
    while(input[i] != '\0' && j < sizeof(result_buffer) - 1)
    {
        if (strlen(result_buffer) >= 8)
            no();
        if (i >= strlen(input))
            no();
        

        ascii_buffer[0] = input[i];
        ascii_buffer[1] = input[i+1];
        ascii_buffer[2] = input[i+2];
        ascii_buffer[3] = '\0';

        result_buffer[j] = (char)atoi(ascii_buffer);
        i+=3;
        j++;
    }
    result_buffer[j] = '\0';

    if (strcmp(result_buffer,"delabere"))
        no();
    else
        printf("Good job.\n");

    return 0;
}