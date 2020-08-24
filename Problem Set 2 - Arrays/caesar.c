#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = strlen(argv[1]) - 1; i >= 0; i--)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

    }

    int key = atoi(argv[1]);

    string plaintext = get_string("plaintext: ");

    char ciphertext[strlen(plaintext)];

    strcpy(ciphertext, plaintext);

    for (int i = strlen(plaintext) - 1; i >= 0; i--)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                ciphertext[i] = (int)((plaintext[i] + key - 65) % 26 + 65);
            }


            if (islower(plaintext[i]))
            {
                ciphertext[i] = (int)((plaintext[i] + key - 97) % 26 + 97);
            }
        }
    }

    printf("ciphertext: %s\n", ciphertext);

    return 0;
}