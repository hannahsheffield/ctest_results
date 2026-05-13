from datetime import datetime
import pandas as pd

from modules import bigquery_functions


class Campaign:
    
    def __init__(
        self,
        name,
        channel_name,
        start_date,
        end_date
    ):
        self.name = name
        self.channel_name = channel_name
        self.start_date = start_date
        self.end_date = end_date

    def get_performance(self):

        if self.channel_name == "network_a":
            data = self.get_performance_standard()

        elif self.channel_name == "network_b":
            data = self.get_performance_standard()

        elif self.channel_name == "network_c":
            data = self.get_performance_standard()

        elif self.channel_name == "network_d":
            data = self.get_performance_cohort()

        else:
            print(
                f"Unsupported channel: {self.channel_name}"
            )
            return pd.DataFrame()

        if len(data) > 0:
            return data

        else:
            print(
                f"No data was found for the campaign: {self.name}."
            )

            return pd.DataFrame()

    def get_performance_standard(self):

        response = bigquery_functions.run_query(
            "GET_STANDARD_CAMPAIGN_PERFORMANCE.sql",
            {
                "PARAM-CAMPAIGN-NAME": self.name,
                "PARAM-START-DATE": self.start_date,
                "PARAM-END-DATE": self.end_date
            }
        )

        return response

    def get_performance_cohort(self):

        response = bigquery_functions.run_query(
            "GET_COHORT_CAMPAIGN_PERFORMANCE.sql",
            {
                "PARAM-CAMPAIGN-NAME": self.name,
                "PARAM-START-DATE": self.start_date,
                "PARAM-END-DATE": self.end_date
            }
        )

        return response
