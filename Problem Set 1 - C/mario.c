#include <cs50.h>
#include <stdio.h>

//Mario less
int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {   
            if (j >= height - i - 1)
            {
                printf("#");
            }  
                

            else
            {
                printf(" ");
            }
                 
        }
        printf("\n");
    }


}
