class Document:
    def __init__(self,name,planet,expiration_date):
        self.name = name
        self.planet = planet
        self.expiration_date = expiration_date

    def is_expired(self, current_year = 2026):
        return self.expiration_date < current_year