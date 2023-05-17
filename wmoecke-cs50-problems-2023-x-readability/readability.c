#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Coleman-Liau index: 0.0588 * L - 0.296 * S - 15.8
    // where L is the average number of letters per 100 words in the text,
    // and S is the average number of sentences per 100 words in the text
    float L = (float)letters / (float)words * 100;
    float S = (float)sentences / (float)words * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Grade the text according to the calculated index
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    // For each character we count the letters (not other symbols)
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]) > 0)
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 0;
    char copy_text[strlen(text)];
    strcpy(copy_text, text); // Make a copy of the input text

    // Tokenize the text with a space as delimiter, adding each token to the count
    char *token = strtok(copy_text, " ");
    while (token != NULL)
    {
        count++;
        token = strtok(NULL, " ");
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    const char delimiters[] = ".!?";
    char copy_text[strlen(text)];
    strcpy(copy_text, text); // Make a copy of the input text

    // Tokenize the text with the delimiters, adding each token to the count
    char *token = strtok(copy_text, delimiters);
    while (token != NULL)
    {
        count += (strlen(token) == 1 && isalpha(token[0]) == 0) ? 0 : 1;
        token = strtok(NULL, delimiters);
    }
    return count;
}