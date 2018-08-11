#!/usr/bin/env python3
from cmd import Cmd
import datetime

import sqlite3
from utils import is_number, is_int


class Buchhalter(Cmd):
    intro = "Welcome to Buchhalter"
    prompt = ">"

    def __init__(self):
        super().__init__()
        self.db = None

    def setup_db(self):
        c = self.db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS entries ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "amount REAL NOT NULL,"
                "type TEXT,"
                "date TEXT,"
                "description TEXT);")
        self.db.commit()

    def preloop(self):
        if self.db is None:
            self.db = sqlite3.connect("buchhalter.db")
            self.db.row_factory = sqlite3.Row

        self.setup_db()


    def postloop(self):
        if self.db is not None:
            self.db.commit()
            self.db.close()
            self.db = None

    def do_add(self, arg):
        'add <amount> [type <type>] [date <date>] [description]'
        amount = self.get_amount()
        t = self.get_type()
        date = self.get_date()
        description = self.get_description()

        c = self.db.cursor()
        c.execute("INSERT INTO entries (amount, type, date, description) "
                "VALUES (?,?,?,?);" , (amount, t, date, description))
        self.db.commit()

    def do_delete(self, arg):
        'delete <id>'

        entry_id = self.get_id()

        c = self.db.cursor()
        c.execute("DELETE FROM entries WHERE id == ?", (entry_id,))
        self.db.commit()


    def do_change(self, arg):
        'change <id> [amount <amount>] [type <type>] [date <date>] [description]'

    def do_show(self, arg):
        'show [limit <number>] [since <date>] [type <type>, ...]'

        limit = self.get_limit()

        c = self.db.cursor()
        query = "SELECT * FROM entries ORDER BY date, id" 
        if limit is not None:
            query += " LIMIT %d" % limit
        c.execute(query)
        result = c.fetchall()

        if len(result) == 0:
            print("no entries available")
            return

        id_size = max(max(len(str(i["id"])) for i in result), len("ID"))
        amount_size = max(max(len(str(int(i["amount"]))) + 3 for i in result), len("amount"))
        type_size = max(max(len(i["type"]) for i in result), len("type"))

        id_template = "{:" + str(id_size) + "d}"
        amount_template = "{:" + str(amount_size) + ".2f}"
        type_template = "{:" + str(type_size) + "}"


        for line in result:
            print(id_template.format(line["id"]), "|",
                    line["date"], "|",
                    amount_template.format(line["amount"]), "|",
                    type_template.format(line["type"]), "|",
                    line["description"])

        income = sum(r["amount"] for r in result if r["amount"] > 0)
        spending = sum(r["amount"] for r in result if r["amount"] < 0 )

        print("income: ", income)
        print("spending: ", spending)
        print("total: ", income + spending)

    def do_quit(self, arg):
        'quit'
        return True
    def do_exit(self, arg):
        'alias for quit'
        return True

    def print_table_head(self):
        pass

    def get_id(self):
        """gets an entry ID from the input, makes error checks and returns it."""
        while(True):
            entry_in = input("ID: ")
            if is_int(entry_in):
                # check if id is in database
                entry_id = int(entry_in)
                c = self.db.cursor()
                c.execute("SELECT id FROM entries WHERE id = ?", (entry_id, ))
                if len(c.fetchall()) == 1:
                    return entry_id
                else:
                    print("ID %d is not in the database", (entry_id,))

            else:
                print("'%s' is not a valid ID")

    def get_date(self):
        while(True):
            date_in = input("date (defaults to today): ")
            if date_in == "":
                return str(datetime.date.today())
            else:
                try:
                    date = datetime.datetime.strptime(date_in, "%Y-%m-%d").date()
                    return str(date)
                except ValueError:
                    print("'%s' is not a valid date format, must be YYYY-MM-DD" % date_in)

    def get_amount(self):
        while(True):
            amount_in = input("amount (negative values for spend money):")
            if is_number(amount_in):
                return float(amount_in)
            else:
                print("'%s' is not a valid number")

    def get_type(self):
        return input("type:")

    def get_description(self):
        return input("description:")

    def get_limit(self):
        while(True):
            limit_in = input("limit: ")
            if limit_in == "":
                return None
            try:
                limit = int(limit_in)
                return limit
            except ValueError:
                print("'%s' is not a valid limit" % (limit_in,))


if __name__ == "__main__":
    Buchhalter().cmdloop()
