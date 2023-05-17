#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            int avg_pixel = round((pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.0);
            pixel.rgbtRed = avg_pixel;
            pixel.rgbtGreen = avg_pixel;
            pixel.rgbtBlue = avg_pixel;

            image[h][w] = pixel;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            RGBTRIPLE pixel = image[h][w];
            int sepiaRed = round(.393 * pixel.rgbtRed + .769 * pixel.rgbtGreen + .189 * pixel.rgbtBlue);
            int sepiaGreen = round(.349 * pixel.rgbtRed + .686 * pixel.rgbtGreen + .168 * pixel.rgbtBlue);
            int sepiaBlue = round(.272 * pixel.rgbtRed + .534 * pixel.rgbtGreen + .131 * pixel.rgbtBlue);

            pixel.rgbtRed = sepiaRed <= 255 ? sepiaRed : 255;
            pixel.rgbtGreen = sepiaGreen <= 255 ? sepiaGreen : 255;
            pixel.rgbtBlue = sepiaBlue <= 255 ? sepiaBlue : 255;

            image[h][w] = pixel;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        int left = 0, right = width - 1;
        while (left < right)
        {
            RGBTRIPLE temp = image[h][left];
            image[h][left] = image[h][right];
            image[h][right] = temp;
            left++;
            right--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int avg_red[height][width];
    int avg_green[height][width];
    int avg_blue[height][width];

    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int avg_r = 0, avg_g = 0, avg_b = 0, neighbor_count = 0;

            // Access the neighbors within 1 row and 1 column and
            // accumulate pixel values for averaging later
            for (int x = -1; x <= 1; x++)
            {
                for (int y = -1; y <= 1; y++)
                {
                    int row = h + x;
                    int col = w + y;

                    // Check if the neighboring pixel is within the bounds
                    if (row >= 0 && row < height && col >= 0 && col < width)
                    {
                        RGBTRIPLE neighbor_pixel = image[row][col];
                        avg_r += neighbor_pixel.rgbtRed;
                        avg_g += neighbor_pixel.rgbtGreen;
                        avg_b += neighbor_pixel.rgbtBlue;
                        neighbor_count++;
                    }
                }
            }

            // Average the pixel values for R, G and B
            avg_red[h][w] = avg_r / neighbor_count;
            avg_green[h][w] = avg_g / neighbor_count;
            avg_blue[h][w] = avg_b / neighbor_count;
        }
    }

    // Apply averaged pixel values to image
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            image[h][w].rgbtRed = avg_red[h][w];
            image[h][w].rgbtGreen = avg_green[h][w];
            image[h][w].rgbtBlue = avg_blue[h][w];
        }
    }
    return;
}
