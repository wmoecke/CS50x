#include <cs50.h>
#include <stdio.h>

void draw_tiles(char sprite, int n);

int main(void)
{
    int n = 0;

    // Get user input for height
    while (n < 1 || n > 8)
    {
        n = get_int("Height: ");
    }

    // Draw the sprite per user input
    for (int row = n - 1; row >= 0; row--)
    {
        draw_tiles(' ', row);
        draw_tiles('#', n - row);
        draw_tiles(' ', 2);
        draw_tiles('#', n - row);
        printf("\n");
    }
}

// Function to draw the tiles in a row according to quantity
void draw_tiles(char tile, int quantity)
{
    for (int i = 0; i < quantity; i++)
    {
        printf("%c", tile);
    }
}