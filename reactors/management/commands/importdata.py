import re
import datetime
import pandas as pd
from reactors.models import Reactor, StatusEntry
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Custom command to import reactor and status entry data into Django model instances."""
    help = "Imports nuclear reactor data from data files provided in 'data' directory."

    def handle(self, *args, **options):
        data_df = pd.read_excel('data/external/reactors-operating.xlsx', converters={'Docket Number': str})
        status_df = pd.read_csv('data/status_w_dockets.csv', converters={'DocketNum': str}, index_col=0)
        dockets_df = pd.read_csv('data/units_and_dockets.csv', converters={'DocketNum': str}, index_col=0)

        def get_clean_val(val):
            """Returns None if the value provided is a Pandas null value, else returns value."""
            return None if pd.isnull(val) else val

        def get_date_from_timestamp(timestamp):
            """Returns datetime.date object from Pandas timestamp value."""
            cleaned_timestamp = get_clean_val(timestamp)
            return cleaned_timestamp.date() if cleaned_timestamp else None

        def get_date_from_string(date_str):
            """Returns datetime.date object from string provided."""
            try:
                return datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
            except ValueError:  # Return None if cell contains a string where there should be a Timestamp value
                return None

        def get_short_name(docket_num_str):
            """
            Returns a unit's 'short name' (as found in 'powerreactorstatusforlast365days.txt') given its docket number.
            """
            return dockets_df.loc[dockets_df['DocketNum'] == docket_num_str, 'Unit'].values[0]

        def parse_city_and_state(location_str):
            """Parses string given and returns city and state."""
            trimmed_location = re.sub('\(.*?\)', '', location_str)  # Ignore text in parentheses
            location_list = trimmed_location.split(', ')
            city_stripped, state_stripped = location_list[0].strip(), location_list[-1].strip()
            return city_stripped, state_stripped

        for _, row in data_df.iterrows():
            # Find short_name from dockets_df
            docket_num = get_clean_val(row['Docket Number'])
            short_name = get_short_name(docket_num) if docket_num else None

            # str -> (str, str)
            location = get_clean_val(row['Location'])
            city, state = parse_city_and_state(location) if location else None

            # int -> str
            cleaned_nrc_region = get_clean_val(row['NRC Region'])
            nrc_region_str = str(cleaned_nrc_region) if cleaned_nrc_region else None

            # int -> float
            cleaned_capacity = get_clean_val(row['Capacity MWe'])
            capacity_float = float(cleaned_capacity) if cleaned_capacity else None

            # str -> datetime.date
            cleaned_renewed_issued = get_clean_val(row['Renewed Operating License Issued'])
            renewed_issued_date = get_date_from_string(cleaned_renewed_issued) if cleaned_renewed_issued else None

            Reactor.objects.create(
                short_name=short_name,
                long_name=get_clean_val(row['Plant Name, Unit Number']),
                web_page=get_clean_val(row['NRC Reactor Unit Web Page']),
                docket_number=docket_num,
                license_number=get_clean_val(row['License Number']),
                city=city,
                state=state,
                nrc_region=nrc_region_str,
                parent_company_utility_name=get_clean_val(row['Parent Company Utility Name']),
                licensee=get_clean_val(row['Licensee']),
                parent_company_website=get_clean_val(row['Parent Company Website']),
                parent_company_notes=get_clean_val(row['Parent Company Notes']),
                reactor_and_containment_type=get_clean_val(row['Reactor and Containment Type']),
                steam_supplier_and_design_type=get_clean_val(row['Nuclear Steam System Supplier and Design Type']),
                architect_engineer=get_clean_val(row['Architect-Engineer']),
                constructor_name=get_clean_val(row['Constructor Name']),
                construction_permit_issued=get_date_from_timestamp(row['Construction Permit Issued']),
                operating_license_issued=get_date_from_timestamp(row['Operating License Issued']),
                commercial_operation=get_date_from_timestamp(row['Commercial Operation']),
                renewed_operating_license_issued=renewed_issued_date,
                operating_license_expires=get_date_from_timestamp(row['Operating License Expires']),
                subsequent_renewed_operating_license_issued=get_date_from_timestamp(
                    row['Subsequent Renewed Operating License Issued']),
                licensed_mwt=get_clean_val(row['Licensed MWt']),
                capacity_mwe=capacity_float
            )

        for _, row in status_df.iterrows():
            # Since no individual reactor data is available for 'Vogtle 4', I decided to not log its status entries.
            # This is because if included, it would not link via FK to a Reactor instance, and may require lots of
            # custom code to accommodate this one instance.
            docket_num = get_clean_val(row['DocketNum'])  # Only 'Vogtle 4' entries don't have a docket number.
            if not docket_num:
                continue

            # str -> datetime.date
            cleaned_report_dt = get_clean_val(row['ReportDt'])
            if cleaned_report_dt:
                report_dt_date = get_date_from_string(cleaned_report_dt.split()[0])
            else:
                report_dt_date = None

            power = get_clean_val(row['Power'])
            reactor = Reactor.objects.get(docket_number=docket_num)

            StatusEntry.objects.create(
                reactor=reactor,
                date=report_dt_date,
                power=power
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully imported all reactor data and status entries.')
        )
