#include <stdio.h>
#include <string.h>

int main()
{
    char input[423];
    char* key = "__stack_check";
    printf("Please enter key: ");
    scanf("%42s",(char*)&input);
    if (strcmp(key,input))
    {
        printf("Nope.\n");
        return(1);
    }
    else
    {
        printf("Good job.\n");
        return 0;
    }
    return 0;
}