from datetime import datetime
class DbEntry:
    """Luokka vastaa kannan entry taulun rakennetta"""

    def __init__(self, entry_id, document_id, account_id, debit, amount, description, row_number):
        self.id = int(entry_id)
        self.document_id = int(document_id)
        self.account_id = int(account_id)
        self.debit = int(debit)
        self.amount = amount
        self.description = description
        self.row_number = int(row_number)
        self.flags = 0

    @property
    def sql_str(self):
        """Funktio palauttaa SQL lauseen, joka lisää entryn kantaan"""
        return "INSERT INTO entry VALUES ({}, {}, {}, {}, {}, '{}', {}, {})".format(self.id, self.document_id,
                                                                                    self.account_id, self.debit,
                                                                                    self.amount, self.description,
                                                                                    self.row_number, self.flags)


    def __str__(self):
        if self.debit:
            amt = self.amount
        else:
            amt = self.amount * -1
        return f"{str(self.id).rjust(3)} " \
               f"{str(self.document_id).rjust(3)} " \
               f"{str(self.row_number).rjust(3)} " \
               f"{str(self.account_id).rjust(3)} " \
               f"{str(self.debit).rjust(3)} " \
               f"{str(amt).rjust(10)}  " \
               f"{self.description}" \



class DbDocument:
    """luokka vastaa kannan document taulun rakennetta"""

    def __init__(self, doc_id, number, period_id, doc_date):
        self.id = int(doc_id)
        self.number = int(number)
        self.period_id = int(period_id)
        self.doc_date = doc_date
        self.entries = []


    def add_entry(self, db_entry):
        """Funktio lisää dokumentille entryn"""
        self.entries.append(db_entry)

    @property
    def sql_str(self):
        """Funktio palauttaa SQL lauseen, joka lisää dokumentin kantaan"""
        return "INSERT INTO document VALUES ({}, {}, {}, {})".format(self.id, self.number, self.period_id,
                                                                     self.doc_date)
    def __str__(self):
        return f"{self.id} {self.number} {datetime.utcfromtimestamp(self.doc_date / 1000).strftime('%d.%m.%Y')} " \
               f"{self.period_id}"

    def __lt__(self, other):
        return self.doc_date < other.doc_date

    def __gt__(self, other):
        return self.doc_date > other.doc_date


class DbPeriod:
    """Luokka vastaa kannan tilikauden "period" rakennetta"""

    def __init__(self, period_id, start_date, end_date, locked):
        self.id = int(period_id)
        self.startDate = start_date
        self.endDate = end_date
        self.locked = int(locked)
        print(self.id, self.startDate, self.endDate, self.locked)
