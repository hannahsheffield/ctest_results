import time
import json
from datetime import datetime, timedelta

import pandas as pd

from modules import bigquery_functions, production_ab_test
from modules.bigquery_upload import upload_dataframe_to_bigquery


class ProductionABTestBatch:

    def __init__(self, number, start_date, end_date):
        """
        Initialise a new instance of the Batch class.

        :param number: An integer representing the batch number.
        """
        self.number = number
        self.start_date = start_date
        self.end_date = end_date

    def get_schedule(self, schedule_table):
        schedule = bigquery_functions.run_query(
            "GET_BATCH_SCHEDULE.sql",
            {
                "PARAM-TEST-BATCH-NUMBER": self.number,
                "PARAM-START-DATE": self.start_date,
                "PARAM-END-DATE": self.end_date,
                "PARAM-SCHEDULE-TABLE": schedule_table
            }
        )

        return schedule

    def get_performance(self):
        performance = bigquery_functions.run_query(
            "GET_BATCH_CAMPAIGNS_PERFORMANCE.sql",
            {
                "PARAM-TEST-BATCH-NUMBER": self.number,
                "PARAM-START-DATE": self.start_date,
                "PARAM-END-DATE": self.end_date
            }
        )

        return performance

    def get_results(self, schedule, performance):
        issues = pd.DataFrame()
        results = pd.DataFrame()

        unique_campaigns = (
            schedule
            .loc[:, [
                "campaign_name",
                "channel_name",
                "start_date",
                "end_date"
            ]]
            .drop_duplicates()
        )

        for index, row in unique_campaigns.iterrows():

            campaign_name = row["campaign_name"]
            channel_name = row["channel_name"]
            start_date = row["start_date"]
            end_date = row["end_date"]

            abtest = production_ab_test.ProductionABTest(
                name=campaign_name,
                channel_name=channel_name,
                start_date=start_date,
                end_date=end_date
            )

            abtest_schedule = schedule.loc[
                schedule["campaign_name"] == campaign_name,
                :
            ]

            abtest_performance = performance.loc[
                performance["campaign_name"] == campaign_name,
                :
            ]

            try:
                abtest_results = abtest.get_results(
                    abtest_schedule,
                    abtest_performance
                )

                formatted_abtest_results = abtest.format_results(
                    abtest_schedule,
                    abtest_results
                )

                results = pd.concat([
                    results,
                    formatted_abtest_results
                ])

            except Exception:
                issue_row = pd.DataFrame(row).transpose()
                issues = pd.concat([issues, issue_row])
        
        output = {
            "results": results,
            "issues": issues
        }

        return output

    def upload_results_to_bq(self, results, results_table):
        existing_results = self.get_existing_results(results_table)

        if existing_results.empty:
            ProductionABTestBatch.upload_data_to_bq(
                results,
                results_table
            )

        else:
            ProductionABTestBatch.handle_existing_results(
                existing_results,
                results
            )

    def get_existing_results(self, results_table):
        existing_results = bigquery_functions.run_query(
            "GET_BATCH_RESULTS.sql",
            {
                "PARAM-TEST-BATCH-NUMBER": str(self.number),
                "PARAM-RESULTS-TABLE": results_table
            }
        )

        return existing_results

    @staticmethod
    def upload_data_to_bq(data, table):
        upload_dataframe_to_bigquery(
            dataframe=data,
            table_id=table,
            project_id="your-gcp-project-id"
        )

        print("Data successfully uploaded.")
    
    @staticmethod
    def handle_existing_results(existing_results, new_results):
        print("Results for this batch already exist:")
        print("Existing results:")
        display(existing_results)

        print("New results:")
        display(new_results)

        print(
            "Check the data and remove existing results if needed."
        )
