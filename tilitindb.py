class dbEntry:
    """Luokka vastaa kannan entry taulun rakennetta"""
    def __init__(self, id, document_id, account_id, debit, amount, description, row_number, flags):
        self.id = int(id)
        self.document_id = int(document_id)
        self.account_id = int(account_id)
        self.debit = int(debit)
        self.amount = abs(float(amount.replace(',', '.').replace(' ', '').strip()))
        self.description = description
        self.row_number = int(row_number)
        self.flags = int(flags)

    def prepare_insert(self):
        """Funktio palauttaa SQL lauseen, joka lisää entryn kantaan"""
        insertString="INSERT INTO entry VALUES ({}, {}, {}, {}, {}, '{}', {}, {})".format(self.id, self.document_id,
                                                                                 self.account_id,  self.debit,
                                                                                 self.amount, self.description,
                                                                                 self.row_number, self.flags)
        return insertString


class dbDocument:
    """luokka vastaa kannan document taulun rakennetta"""
    def __init__(self, id, number, period_id, doc_date):
        self.id = int(id)
        self.number = int(number)
        self.period_id = int(period_id)
        self.doc_date = doc_date
        self.entries = []

    def add_entry(self, dbEntry):
        """Funktio lisää dokumentille entryn"""
        self.entries.append(dbEntry)

    def prepare_insert(self):
        """Funktio palauttaa SQL lauseen, joka lisää dokumentin kantaan"""
        insertString="INSERT INTO document VALUES ({}, {}, {}, {})".format(self.id, self.number, self.period_id,
                                                                     self.doc_date)
        return insertString

class dbPeriod:
    """Luokka vastaa kannan tilikauden "period" rakennetta"""
    def __init__(self, id, startDate, endDate, locked):
        self.id = int(id)
        self.startDate = startDate
        self.endDate = endDate
        self.locked = int(locked)


