from cs50 import get_string
import re


def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Coleman-Liau index: 0.0588 * L - 0.296 * S - 15.8
    # where L is the average number of letters per 100 words in the text,
    # and S is the average number of sentences per 100 words in the text
    L = letters / words * 100
    S = sentences / words * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Grade the text according to the calculated index
    if (index < 1):
        print("Before Grade 1")
    elif (index >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(text):
    # For each character we count the letters (not other symbols)
    count = 0
    for i in range(len(text)):
        if text[i].isalpha():
            count += 1
    return count


def count_words(text):
    # Tokenize the text with a space as delimiter
    tokenized = text.split()
    return len(tokenized)


def count_sentences(text):
    # Tokenize the text with the delimiters
    tokenized = re.split("[.!?]", text)
    for i in range(len(tokenized)):
        if tokenized[i] == '' or (len(tokenized[i]) == 1 and tokenized[i].isalpha() == False):
            del tokenized[i]
    return len(tokenized)


if __name__ == "__main__":
    main()