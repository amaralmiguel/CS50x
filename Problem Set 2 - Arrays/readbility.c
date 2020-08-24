#include <stdio.h>
#include <math.h>
#include <string.h>
#include <cs50.h>

int main(void)
{
    int letters = 1, sentences = 0, words = 1;

    string input = get_string("Put your text here: ");


    for (int i = strlen(input); i > 0; i--)
    {
        if (input[i] == ' ')
        {
            words++;
        }

        if (input[i] == '!' || input[i] == '?' || input[i] == '.')
        {
            sentences++;
        }

        if (((int) input[i] >= 97 && (int) input[i] <= 122) || ((int) input[i] >= 65 && (int) input[i] <= 90))
        {
            letters++;
        }
    }

    float L = (100 * (float) letters) / (float) words;
    float S = (100 * (float) sentences) / (float) words;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int result = round(index);



    if (result >= 16)
    {
        printf("Grade 16+\n");
    }

    else if (result < 1)
    {
        printf("Before Grade 1\n");
    }

    else
    {
        printf("Grade %i\n", result);
    }

    return 0;
}