#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

void cipher_text(string text, string key);

int main(int argc, string argv[])
{
    // Validate if an argument (key) was supplied
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    int n = strlen(argv[1]);

    // Validate if key has correct length
    if (n != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Validate if supplied key contains only alphabetical characters,
    // and also make all characters uppercase
    for (int i = 0; i < n; i++)
    {
        if (isalpha(argv[1][i]) == 0)
        {
            printf("Key must contain only alphabetical characters.\n");
            return 1;
        }
        else
        {
            argv[1][i] = toupper(argv[1][i]);
        }
    }

    // Validate if there's no duplicate chars in supplied key
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (argv[1][j] == argv[1][i])
            {
                printf("Key must not contain duplicate letters.\n");
                return 1;
            }
        }
    }

    string plaintext = get_string("plaintext: ");   // Get user input
    cipher_text(plaintext, argv[1]);
    printf("ciphertext: %s\n", plaintext);
}

// Function to cipher the plaintext in place
void cipher_text(string text, string key)
{
    const string ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int n = strlen(text);

    // Iterate through plaintext, replacing characters
    // according to supplied key
    for (int i = 0; i < n; i++)
    {
        if (isalpha(text[i]) > 0)   // Only consider alphabet letters
        {
            char letter = toupper(text[i]);
            int pos = strcspn(ALPHABET, &letter);
            if (isupper(text[i]) > 0) // Uppercase char
            {
                text[i] = key[pos];
            }
            else if (islower(text[i]) > 0) // Lowercase char
            {
                text[i] = tolower(key[pos]);
            }
        }
    }
}