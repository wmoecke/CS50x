#include <stdio.h>
#include <cs50.h>
#include <math.h>

long get_checksum(long n, int length);
void identify_card_issuer(long n, int length);

int main(void)
{
    long n = get_long("Number: ");

    // Calculate the number's length
    int exp = (int)ceil(log10(n));

    // Get the checksum then check for validity
    long sum = get_checksum(n, exp);
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // 'Nuff said
    identify_card_issuer(n, exp);
}

long get_checksum(long n, int length)
{
    // Convert the number to a string
    char str[length];
    sprintf(str, "%ld", n);

    long times_two[length / 2];
    long sum = 0;
    int count = 0;

    // Multiply every other digit by 2, starting
    // with the number's second-to-last digit
    for (int i = length - 2; i >= 0; i -= 2)
    {
        int x = (str[i] - '0');
        times_two[count] = x * 2;
        count++;
    }

    // Add those products' digits (not the
    // products themselves) together
    for (int i = 0; i < count; i++)
    {
        while (times_two[i] > 0)
        {
            sum += times_two[i] % 10;
            times_two[i] /= 10;
        }
    }

    // Add the previous sum to the sum of the digits that
    // weren't multiplied by 2 (starting from the end)
    for (int i = length - 1; i >= 0; i -= 2)
    {
        int x = (str[i] - '0');
        sum += x;
    }

    return sum;
}

void identify_card_issuer(long n, int length)
{
    // Convert the number to a string
    char str[length];
    sprintf(str, "%ld", n);

    // Get first and second digits as integers
    int d1 = (str[0] - '0');
    int d2 = (str[1] - '0');

    // Identify issuer according to card
    // length and first 2 digits
    switch (length)
    {
        case 15:
            if (d1 == 3 && (d2 == 4 || d2 == 7))
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
            break;
        case 13:
        case 16:
            switch (d1)
            {
                case 4:
                    printf("VISA\n");
                    break;
                case 5:
                    if (length == 16 && (d2 == 1 || d2 == 2 || d2 == 3 || d2 == 4 || d2 == 5))
                    {
                        printf("MASTERCARD\n");
                    }
                    else
                    {
                        printf("INVALID\n");
                    }
                    break;
                default:
                    printf("INVALID\n");
                    break;
            }
            break;
        default:
            printf("INVALID\n");
            break;
    }
}