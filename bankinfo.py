import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tilitin_import.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class bankinfo:
    """Luokka pankkikohtaisille asetuksille"""
    def __init__(self, binfo):
        self.set_values(bank)
        logger.info('BankInfo CREATED')
        
    def set_values(self, bank):
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
        else:
            user_defined()


    def user_defined(self):
        """Käyttäjän vapaasti määriteltävät pankki-csv asetukset"""
        logger.info('bankInfo, USER DEF CREATED')
        delimiter = input("Kenttäerotin [,]:") or ","
        timeformat = input("Timeformat [%d.%m.%Y]:") or "%d.%m.%Y"
        datecolumn = input("Päivämäärän sarake [0]:") or 0
        sumcolumn = input("Summan sarake [2]:") or 2
        desc_column = input("Kuvauksen sarake [1]:") or 1
        self.delimiter =  delimiter,
        self.timeformat = timeformat,
        self.datecol = int(datecolumn),
        self.sumcol =int(sumcolumn),
        self.descol =int(desc_column)
        return None
