class DbEntry:
    """Luokka vastaa kannan entry taulun rakennetta"""

    def __init__(self, entry_id, document_id, account_id, debit, amount, description, row_number):
        self.id = int(entry_id)
        self.document_id = int(document_id)
        self.account_id = int(account_id)
        self.debit = int(debit)
        self.amount = abs(float(amount.replace(',', '.').replace(' ', '').strip()))
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


class DbDocument:
    """luokka vastaa kannan document taulun rakennetta"""

    def __init__(self, doc_id, number, period_id, doc_date):
        self.id = int(doc_id)
        self.number = int(number)
        self.period_id = int(period_id)
        self.doc_date = doc_date
        self.entries = []

    def __lt__(self, other):
        return self.doc_date < other.doc_date

    def add_entry(self, db_entry):
        """Funktio lisää dokumentille entryn"""
        self.entries.append(db_entry)

    @property
    def sql_str(self):
        """Funktio palauttaa SQL lauseen, joka lisää dokumentin kantaan"""
        return "INSERT INTO document VALUES ({}, {}, {}, {})".format(self.id, self.number, self.period_id,
                                                                     self.doc_date)


class DbPeriod:
    """Luokka vastaa kannan tilikauden "period" rakennetta"""

    def __init__(self, period_id, start_date, end_date, locked):
        self.id = int(period_id)
        self.startDate = start_date
        self.endDate = end_date
        self.locked = int(locked)
        print(self.id, self.startDate, self.endDate, self.locked)
