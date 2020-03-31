
class account: # implements Comparable<Account> {

    def __init__(self, id, name, type, vatCode, vatRate, vatAccount1Id, vatAccount2Id, flags, number):
        self.id = id
        self.name = name
        self.type = type
        self.vatCode = vatCode
        self.vatRate = vatRate
        self.vatAccount1Id = vatAccount1Id
        self.vatAccount2Id = vatAccount2Id
        self.flags = flags
        self.number = number
