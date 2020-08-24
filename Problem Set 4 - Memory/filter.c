#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Declaring the original pixel colors variables
    unsigned int originalRed, originalGreen, originalBlue, grayPixel;

    // Running trough the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Getting the original pixel colors
            originalRed = image[i][j].rgbtRed;
            originalGreen = image[i][j].rgbtGreen;
            originalBlue = image[i][j].rgbtBlue;

            // The Gray Scale of a Pixel is the avarage of the RGB colors of the Pixel
            grayPixel = round((originalRed + originalGreen + originalBlue) / 3.0);

            // Applying Gray Scale Filter on each pixel of an image
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = grayPixel;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // The unsigned int garants that values are always positive numbers
    unsigned int sepiaRed, sepiaGreen, sepiaBlue;

    // Declaring the original pixel colors variables
    int originalRed, originalGreen, originalBlue;

    // Running trough the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Getting the original pixel colors
            originalRed = image[i][j].rgbtRed;
            originalGreen = image[i][j].rgbtGreen;
            originalBlue = image[i][j].rgbtBlue;

            // Getting Sepia values
            sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            // Ensure that not pass 255 value
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Applying Sepia Filter on each pixel of an image
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Making a struct RGBTRIPLE copy for swap
    RGBTRIPLE swapPixel;

    // Running trough the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swaping the pixels
            swapPixel = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = swapPixel;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Making a struct RGBTRIPLE copy
    RGBTRIPLE copy[height][width];

    // Declaring the needed variables
    int sumRed, sumGreen, sumBlue;
    float counter;

    // Running trough the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Restarting the values to 0 when the processe with one pixel is done
            sumRed = sumGreen = sumBlue = 0;
            counter = 0;

            // Running trough Pixel by Pixel in each corner
            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    // Continue if colides the corner
                    if (i + h < 0 || i + h > height - 1 || j + w < 0 || j + w > width - 1)
                    {
                        continue;
                    }

                    // Counting the RGB values
                    sumRed += image[i + h][j + w].rgbtRed;
                    sumGreen += image[i + h][j + w].rgbtGreen;
                    sumBlue += image[i + h][j + w].rgbtBlue;

                    counter ++;
                }
            }

            // Making the Avarage of the RGB values
            copy[i][j].rgbtRed = round(sumRed / counter);
            copy[i][j].rgbtGreen = round(sumGreen / counter);
            copy[i][j].rgbtBlue = round(sumBlue / counter);
        }
    }

    // Applying the Blur effect to the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = copy[i][j].rgbtRed;
            image[i][j].rgbtGreen = copy[i][j].rgbtGreen;
            image[i][j].rgbtBlue = copy[i][j].rgbtBlue;
        }
    }

    return;
}
