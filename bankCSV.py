class bankinfo:
    """Luokka pankkikohtaisille astuksille"""
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