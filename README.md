# buchhalter
buchhalter is a small cli application for very simple personal accounting.

it has no dependencies other than python 3.
Your data is stored in a SQLite3 database.

# How to use it

## commands

    add <amount> [type <type>] [date <date>] [description]

Adds an amount of money (you received money).
`type` allows you to categorize the money you received.
`date` specifies the date on which you have gotten that money.
If you omit the `date` parameter today is assumed.

    sub <amount> [type <type>] [date <date>] [description]

Does the same as the add command but for spending money.

	delete <id>

deletes the position with the given id.

	change [amount <amount>] [type <type>] [date <date>] [description]

changes some of the values. if you omit one it is left the way it was.

	show [limit <number>] [since <date>] [type <type>, ...]

shows you all positions in the database and gives you the total amount of money you
received and spend.
`limit` limites the output (and the total amount) to the last `<number>` positions
`since` limites the output to all positions since `<date>`
`type` limites the output to only positions with the given types

## arguments

`<type>` is any string. It is used to categorize things.
`<amount` is a amount of money. real values are separated by a dot. Valid values are e.g. 10.1, 1337, 5, -10, -0.5
`<date>` is a date given in the YYYY-MM-DD notation. e.g. 2018-07-06 would be the 6th. of July 2018.
