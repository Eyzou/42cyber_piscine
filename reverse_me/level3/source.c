//the strin is ********
// begin by 42
//then first of the buffer is *
// then convert to ASCI 42042042042042042042042
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
    char input[43];
    char result_buffer[9];
    char ascii_buffer[4];

    printf("Please enter key: ");
    if (scanf("%42s",input) != 1)
        no();

    if (input[0] != '4' || input[1] != '2')
        no();

    fflush(stdout);

    memset(result_buffer,0, sizeof(result_buffer));
    result_buffer[0] ='*';

    unsigned int i = 2; // car ya deja 42
    unsigned int j = 1; // car ya deja un * 

    while (1)
    {
        if (strlen(result_buffer) >= 8)
            break;

        if (i >= strlen(input))
            break;

        ascii_buffer[0] = input[i];
        ascii_buffer[1] = input[i+1];
        ascii_buffer[2] = input[i+2];
        ascii_buffer[3] = '\0';

        result_buffer[j] = (char)atoi(ascii_buffer);
        i+=3;
        j++;
    }
    result_buffer[j] = '\0';

    if (strcmp(result_buffer,"********"))
        no();
    else
        printf("Good job.\n");

    return 0;
}