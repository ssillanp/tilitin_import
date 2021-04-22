class bankinfo:
    """Luokka pankkikohtaisille asetuksille"""
    def __init__(self, bank):
        self.set_values(self, bank)
        
    def set_values(bank):
        if bank == 'op':
            self.delimiter =  ';'
            self.timeformat = '%d.%m.%Y'
            self.datecol = 0
            self.sumcol = 2
            self.descol = 6        
        elif bank == 'danske':
            self.delimiter = ';'
            self.timeformat = '%d.%m.%Y'
            self.datecol = 0
            self.sumcol = 2
            self.descol = 1
#         elif bank == 'nordea':
#             self.delimiter = ';'
#             self.timeformat = '%d.%m.%Y'
#             self.datecol = 0
#             self.sumcol = 1
#             self.descol = 5
#         else:
#             user_defined()


#     def user_defined(self):
#         """Käyttäjän vapaasti määriteltävät pankki-csv asetukset"""
#         delimiter = input("Kenttäerotin [,]:") or ","
#         timeformat = input("Timeformat [%d.%m.%Y]:") or "%d.%m.%Y"
#         datecolumn = input("Päivämäärän sarake [0]:") or 0
#         sumcolumn = input("Summan sarake [2]:") or 2
#         desc_column = input("Kuvauksen sarake [1]:") or 1
#         self.user = {
#             'delimiter': delimiter,
#             'timeformat': timeformat,
#             'datecol': int(datecolumn),
#             'sumcol': int(sumcolumn),
#             'descol': int(desc_column)
#         }
#         return self.user
