// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
// N = ceil(143092 / 0.5)
const unsigned int N = 286184;

// Hash table
node *table[N];

// Items count
unsigned int num_words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Searches for word in the hash table (case-insensitive)
    node *next = table[hash(word)];
    while (next)
    {
        if (strcasecmp(word, next->word) == 0)
        {
            return true;
        }
        next = next->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hashes a word by summing its ASCII character
    // codes and modulo'ing with N.
    unsigned int hash = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hash += tolower(word[i]);
    }
    return hash % N;
}

// Loads dictionary into memory, returning
// true if successful, else false
bool load(const char *dictionary)
{
    // Load the data set of words
    FILE *f = fopen(dictionary, "r");
    if (f == NULL)
    {
        return false;
    }

    // Scans the dictionary, line by line,
    // storing each word in the linked list array
    char line[LENGTH + 1];
    while (fscanf(f, "%s", line) != EOF)
    {
        // Allocate memory for new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // Store word in new node and
        // fit it into the hash table
        strcpy(n->word, line);
        unsigned int hashed = hash(line);
        n->next = table[hashed];
        table[hashed] = n;

        // Stored words counter
        num_words++;
    }
    fclose(f);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return num_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *next = table[i];
        while (next)
        {
            node *current = next;
            next = next->next;
            free(current);
        }
    }
    return true;
}
