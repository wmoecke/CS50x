-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Get the report from the given date and place
SELECT description
  FROM crime_scene_reports
 WHERE day = 28
   AND month = 7
   AND year = 2021
   AND LOWER(street) LIKE '%humphrey street%';
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
-- Littering took place at 16:36. No known witnesses.

-- Get the witnessess' interviews transcripts
SELECT name, transcript
  FROM interviews
 WHERE day = 28
   AND month = 7
   AND year = 2021;
-- Ruth    : Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
--           If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- Eugene  : I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--           I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- Raymond : As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
--           In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
--           The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Checking first clue: Bakery security footage
SELECT activity, license_plate, hour, minute
  FROM bakery_security_logs
 WHERE day = 28
   AND month = 7
   AND year = 2021
   AND hour = 10
   AND minute BETWEEN 15 AND 25;

-- Checking second clue: ATM transaction logs
SELECT account_number
  FROM atm_transactions
 WHERE day = 28
   AND month = 7
   AND year = 2021
   AND LOWER(atm_location) LIKE '%leggett street%'
   AND transaction_type = 'withdraw';

-- Checking third clue: Phone call logs
SELECT caller, receiver
  FROM phone_calls
 WHERE day = 28
   AND month = 7
   AND year = 2021
   AND duration < 60;

-- Finding possible suspects: Joining the queries
SELECT name, passport_number
  FROM people ppl
       JOIN bank_accounts bnk
       ON bnk.person_id = ppl.id
 WHERE bnk.account_number IN
       (SELECT account_number
          FROM atm_transactions
         WHERE day = 28
           AND month = 7
           AND year = 2021
           AND LOWER(atm_location) LIKE '%leggett street%'
           AND transaction_type = 'withdraw')
   AND ppl.license_plate IN
       (SELECT license_plate
          FROM bakery_security_logs
         WHERE day = 28
           AND month = 7
           AND year = 2021
           AND hour = 10
           AND minute BETWEEN 15 AND 25
           AND activity = 'exit')
   AND ppl.phone_number IN
       (SELECT caller
          FROM phone_calls
         WHERE day = 28
           AND month = 7
           AND year = 2021
           AND duration < 60);
--+-------+-----------------+
--| name  | passport_number |
--+-------+-----------------+
--| Bruce | 5773159633      |
--| Diana | 3592750733      |
--+-------+-----------------+

-- Narrowing down our suspects list: Looking for early flights out of Fiftyville the next day
SELECT ppl.name, ori.city AS origin, des.city AS destination, flt.hour, flt.minute
  FROM people ppl
       JOIN passengers psg
       ON psg.passport_number = ppl.passport_number
       JOIN flights flt
       ON flt.id = psg.flight_id
       JOIN airports ori
       ON ori.id = flt.origin_airport_id
       JOIN airports des
       ON des.id = flt.destination_airport_id
 WHERE ppl.passport_number IN ('5773159633', '3592750733')
   AND flt.day = 29
   AND flt.month = 7
   AND flt.year = 2021
   AND LOWER(ori.city) = 'fiftyville';
--+-------+------------+---------------+------+--------+
--| name  |   origin   |  destination  | hour | minute |
--+-------+------------+---------------+------+--------+
--| Diana | Fiftyville | Boston        | 16   | 0      |
--| Bruce | Fiftyville | New York City | 8    | 20     |
--+-------+------------+---------------+------+--------+
-- Bruce is our thief! And he flew to NYC!

-- Now on to find Bruce's accomplice
SELECT ppl.name
  FROM people ppl
 WHERE ppl.phone_number IN
       (SELECT phc.receiver
          FROM phone_calls phc
         WHERE phc.day = 28
           AND phc.month = 7
           AND phc.year = 2021
           AND phc.duration < 60
           AND phc.caller =
               (SELECT phone_number
                  FROM people
                 WHERE passport_number = '5773159633'));
--+-------+
--| name  |
--+-------+
--| Robin |
--+-------+
