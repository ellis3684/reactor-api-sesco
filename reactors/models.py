import datetime
from django.db import models


class Reactor(models.Model):
    """Individual reactor data as listed in 'reactors-operating.xlsx'."""
    short_name = models.CharField(max_length=200, unique=True)  # Name used in 'powerreactorstatusforlast365days.txt'
    long_name = models.CharField(max_length=200, unique=True)  # Name used in Excel doc
    web_page = models.CharField(max_length=200)
    docket_number = models.CharField(max_length=8, unique=True)  # Unique identifier for each reactor
    license_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    nrc_region = models.CharField(max_length=10)
    parent_company_utility_name = models.CharField(max_length=200)
    licensee = models.CharField(max_length=200)
    parent_company_website = models.CharField(max_length=200)
    parent_company_notes = models.TextField(null=True)
    reactor_and_containment_type = models.CharField(max_length=50)
    steam_supplier_and_design_type = models.CharField(max_length=50)
    architect_engineer = models.CharField(max_length=50)
    constructor_name = models.CharField(max_length=50)
    construction_permit_issued = models.DateField(null=True)
    operating_license_issued = models.DateField(null=True)
    commercial_operation = models.DateField(null=True)
    renewed_operating_license_issued = models.DateField(null=True)
    operating_license_expires = models.DateField(null=True)
    subsequent_renewed_operating_license_issued = models.DateField(null=True)
    licensed_mwt = models.FloatField()
    capacity_mwe = models.FloatField()

    @classmethod
    def get_days_str_repr(cls, end_date, start_date):
        days = (end_date - start_date).days
        years = days // 365
        if years == 0:
            return f'{days} days'
        elif years == 1:
            return f'{years} years'
        return f'{years} years'

    @property
    def license_length(self):
        """Returns a timedelta object of the difference between the operating license issued and expiry dates."""
        if not self.operating_license_expires or not self.operating_license_issued:
            return
        return self.get_days_str_repr(self.operating_license_expires, self.operating_license_issued)

    @property
    def current_reactor_age(self):
        """Returns a timedelta object of the difference between today and the operating license issued date."""
        if not self.operating_license_issued:
            return
        return self.get_days_str_repr(datetime.datetime.today().date(), self.operating_license_issued)

    @property
    def time_remaining(self):
        """Returns a timedelta object of the difference between today and the operating license expiry date."""
        if not self.operating_license_expires:
            return
        return self.get_days_str_repr(self.operating_license_expires, datetime.datetime.today().date())


class StatusEntry(models.Model):
    """Status entry for a particular date as listed in 'powerreactorstatusforlast365days.txt'."""
    reactor = models.ForeignKey(Reactor, on_delete=models.CASCADE)
    date = models.DateField()
    power = models.SmallIntegerField()

    class Meta:
        constraints = [
            # Only one entry per reactor per date
            models.UniqueConstraint(fields=['reactor', 'date'], name='reactor_and_date_unique')
        ]
