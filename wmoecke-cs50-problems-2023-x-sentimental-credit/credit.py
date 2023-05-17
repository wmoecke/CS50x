from cs50 import get_string


def main():
    n = get_string("Number: ")

    # Get the checksum then check for validity
    sum = get_checksum(n, len(n))
    if sum % 10 != 0:
        print("INVALID")
        return 0

    # 'Nuff said
    identify_card_issuer(n, len(n))


def get_checksum(n, length):
    times_two = []
    sum = 0

    # Multiply every other digit by 2, starting
    # with the number's second-to-last digit
    for i in range(length - 2, -1, -2):
        x = int(n[i])
        times_two.append(x * 2)

    # Add those products' digits (not the
    # products themselves) together
    for i in range(len(times_two)):
        digits = [int(x) for x in str(times_two[i])]
        for j in range(len(digits)):
            sum += digits[j]

    # Add the previous sum to the sum of the digits that
    # weren't multiplied by 2 (starting from the end)
    for i in range(length - 1, -1, -2):
        x = int(n[i])
        sum += x

    return sum


def identify_card_issuer(n, length):
    # Get first and second digits as integers
    d1 = int(n[0])
    d2 = int(n[1])

    # Identify issuer according to card
    # length and first 2 digits
    match length:
        case 15:
            if d1 == 3 and (d2 == 4 or d2 == 7):
                print("AMEX")
            else:
                print("INVALID")
        case 13 | 16:
            match d1:
                case 4:
                    print("VISA")
                case 5:
                    if length == 16 and (d2 == 1 or d2 == 2 or d2 == 3 or d2 == 4 or d2 == 5):
                        print("MASTERCARD")
                    else:
                        print("INVALID")
                case _:
                    print("INVALID")
        case _:
            print("INVALID")


if __name__ == "__main__":
    main()