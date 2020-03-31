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