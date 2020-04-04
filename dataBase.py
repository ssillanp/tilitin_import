class DataBase:
    def __init__(self):
        self.documents = []

    def add_document(self, dbDocument):
        self.documents.append(dbDocument)

    # def list_documents(self):
    #     for doc in self.documents:
    #          return doc

class dbEntry:
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
        insertString="INSERT INTO entry VALUES ({}, {}, {}, {}, {}, '{}', {}, {})".format(self.id, self.document_id,
                                                                                 self.account_id,  self.debit,
                                                                                 self.amount, self.description,
                                                                                 self.row_number, self.flags)
        return insertString

class dbDocument:
    def __init__(self, id, number, period_id, doc_date):
        self.id = id
        self.number = number
        self.period_id = period_id
        self.doc_date = doc_date
        self.entries = []

    def add_entry(self, dbEntry):
        self.entries.append(dbEntry)

    def prepare_insert(self):
        insertString="INSERT INTO document VALUES ({}, {}, {}, {})".format(self.id, self.number, self.period_id,
                                                                     self.doc_date)
        return insertString

class dbPeriod:
    def __init__(self, id, startDate, endDate, locked):
        self.id = id
        self.startDate = startDate
        self.endDate = endDate
        self.locked = locked

    def prepare_insert(self):
        insertString = "INSERT INTO period VALUES ({}, {}, {}, {})".format(self.id, self.startDate, self.endDate,
                                                                       self.locked)
        return insertString

