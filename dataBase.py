class DataBase:
    def __init__(self):
        pass

class entry:
    def __init__(self, id, document_id, account_id, debit, amount, description, row_number, flags):
        self.id = id
        self.document_id = document_id
        self.account_id = account_id
        self.debit = debit
        self.amount = amount
        self.description = description
        self.row_number = row_number
        self.flags = flags

class document:
    def __init__(self, id, number, period_id, doc_date ):
        self.id = id
        self.number = number
        self.period_id = period_id
        self.doc_date = doc_date

class dbPeriod:
    def __init__(self, id, startDate, endDate, locked):
        self.id = id
        self.startDate = startDate
        self.endDate = endDate
        self.locked = locked
