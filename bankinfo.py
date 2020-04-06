class bankinfo:
    """Luokka pankkikohtaisille asetuksille"""
    def __init__(self):
        self.op = {
            'delimiter': ';',
            'timeformat': '%d.%m.%Y',
            'datecol': 0,
            'sumcol': 2,
            'descol': 6
        }

        self.danske = {
            'delimiter': ',',
            'timeformat': '%d.%m.%Y',
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
        delimiter = input("Kenttäerotin [,]:") or ","
        timeformat = input("Timeformat [%d.%m.%Y]:") or "%d.%m.%Y"
        datecolumn = input("Päivämäärän sarake [0]:") or 0
        sumcolumn = input("Summan sarake [2]:") or 2
        desc_column = input("Kuvauksen sarake [1]:") or 1
        self.user = {
            'delimiter': delimiter,
            'timeformat': timeformat,
            'datecol': int(datecolumn),
            'sumcol': int(sumcolumn),
            'descol': int(desc_column)
        }
        return self.user