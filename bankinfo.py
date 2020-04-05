class bankinfo:
    """Luokka pankkikohtaisille asetuksille"""
    def __init__(self):
        self.op = {
            'delimiter': ';',
            'timeformat': '%d.%m.%Y',
            'datecol': 0,
            'sumcol': 1,
            'descol': 5
        }

        self.danske = {
            'delimiter': ',',
            'timeformat': '%m/%d/%y',
            'datecol': 0,
            'sumcol': 2,
            'descol': 1
        }

        # self.nordea = {
        #     'delimiter': ';',
        #     'timeformat': '%d.%m.%Y',
        #     'datecol': 0,
        #     'sumcol': 1,
        #     'descol': 5
        # }

    def user_defined(self):
        """Käyttäjän vapaasti määriteltävät pankki-csv asetukset"""
        delimiter = input("Kenttäerotin: ")
        timeformat = input("Timeformat: ")
        datecolumn = int(input("Päivämäärän sarake: "))
        sumcolumn = int(input("Summan sarake: "))
        desc_column = int(input("Kuvauksen sarake: "))
        self.user = {
            'delimiter': delimiter,
            'timeformat': timeformat,
            'datecol': datecolumn,
            'sumcol': sumcolumn,
            'descol': desc_column
        }
        return self.user