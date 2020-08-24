#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512
#define FILE_NAME_SIZE 8

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Declaring the needed variables
    int file_index = 0;
    char file_name[8]; // 000.jpeg
    BYTE buffer[BLOCK_SIZE];

    // Avoid to incorrect inputs
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the memory card file
    FILE *infile = fopen(argv[1], "r");

    // Avoid the NULL files
    if (infile == NULL)
    {
        return 2;
    }

    // Create an output file, starting with NULL
    FILE *outfile = NULL;


    while (fread(buffer, BLOCK_SIZE, 1, infile) || feof(infile) == 0)
    {
        // check if a JPEG has found
        bool containsJpegHeader = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;

        if (containsJpegHeader)
        {
            // close the file if is not NULL
            if (outfile != NULL)
            {
                fclose(outfile);
            }

            // Create a new file with name ###.jpg
            sprintf(file_name, "%03i.jpg", file_index ++);
            outfile = fopen(file_name, "w");
        }

        // Write the .jpg informations in output file
        if (outfile != NULL)
        {
            fwrite(buffer, sizeof(buffer), 1, outfile);
        }
    }

    // close last jpeg file
    fclose(outfile);

    // close infile
    fclose(infile);

    // success
    return 0;
}
