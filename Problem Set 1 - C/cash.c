#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float troco;
    
    do
    {
        troco = get_float("Change: ");
    }
    while (troco < 0);

    int cents = round(troco * 100);

    int moedas = 0;

    while (cents >= 25)
    {
        cents -= 25;
        moedas++;
    }

    while (cents >= 10)
    {
        cents -= 10;
        moedas++;
    }

    while (cents >= 5)
    {
        cents -= 5;
        moedas++;
    }

    while (cents >= 1)
    {
        cents -= 1;
        moedas++;
    }
     
    printf("%i\n", moedas);
    return 0;

}
