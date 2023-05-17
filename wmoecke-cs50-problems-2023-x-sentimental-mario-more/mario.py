from cs50 import get_int


def main():
    n = 0

    # Get user input for height
    while n < 1 or n > 8:
        n = get_int("Height: ")

    # Draw the sprite per user input
    for row in range(n - 1, -1, -1):
        draw_tiles(' ', row)
        draw_tiles('#', n - row)
        draw_tiles(' ', 2)
        draw_tiles('#', n - row)
        print()


def draw_tiles(tile, quantity):
    """Function to draw the tiles in a row according to quantity"""
    for i in range(quantity):
        print(tile, end='')


if __name__ == "__main__":
    main()