#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"


int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: %s input.wav output.wav\n", argv[0]);
        return 1;
    }

    // Open input file for reading
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file \"%s\".\n", argv[1]);
        return 1;
    }

    // Read header into an array
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    if (check_format(header) == 1)
    {
        printf("Input is not a WAV file.\n");
        return 1;
    }

    long start_of_data = ftell(input);

    // Open output file for writing
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file \"%s\".\n", argv[2]);
        return 1;
    }

    // Write header to file
    if (fwrite(&header, sizeof(WAVHEADER), 1, output) != 1)
    {
        printf("Could not write header to file.\n");
        return 1;
    }

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(header);

    // Move the file pointer to the beginning of the last block of data
    fseek(input, 0 - block_size, SEEK_END);

    // Write reversed audio to file
    while (ftell(input) >= start_of_data)
    {
        WORD block[block_size];
        fread(&block, block_size, 1, input);
        fwrite(&block, block_size, 1, output);
        fseek(input, 0 - (2 * block_size), SEEK_CUR);
    }

    // Close files
    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    const int FORMAT_SIZE = 4;

    // Check for the "WAVE" char sequence in header
    for (int i = 0; i < FORMAT_SIZE; i++)
    {
        switch (i)
        {
            case 0:
                if (header.format[i] != 'W')
                {
                    return 1;
                }
                break;
            case 1:
                if (header.format[i] != 'A')
                {
                    return 1;
                }
                break;
            case 2:
                if (header.format[i] != 'V')
                {
                    return 1;
                }
                break;
            case 3:
                if (header.format[i] != 'E')
                {
                    return 1;
                }
                break;
            default:
                return 1;
                break;
        }
    }
    return 0;
}

int get_block_size(WAVHEADER header)
{
    return header.blockAlign;
}