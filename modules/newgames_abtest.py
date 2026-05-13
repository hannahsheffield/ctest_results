import re

from modules.abtest import ABTest
from modules.config import EXPERIMENTAL_RESULTS_COLUMNS
from modules import bigquery_functions
from modules.bigquery_upload import upload_dataframe_to_bigquery


class ExperimentalABTest(ABTest):
    def __init__(self, name, network, start_date=None, end_date=None):
        super().__init__(name, network, start_date, end_date)

    def format_test_evaluation(self):
        evaluation = ExperimentalABTest.drop_unnecessary_columns(
            self.evaluation
        )

        evaluation_add_columns = self.create_additional_columns(
            evaluation
        )

        evaluation_renamed_cols = ExperimentalABTest.rename_columns(
            evaluation_add_columns
        )

        evaluation_sorted_cols = ExperimentalABTest.sort_columns(
            evaluation_renamed_cols
        )

        evaluation_sorted_cols = evaluation_sorted_cols.convert_dtypes()

        return evaluation_sorted_cols

    @staticmethod
    def drop_unnecessary_columns(df):
        drop_df = df.drop(
            columns=[
                "creative_link",
                "creative_name",
                "day_2_retention",
                "iti_error",
                "z_score",
                "p_value",
                "standard_error",
                "ci_lower",
                "ci_upper",
            ],
            errors="ignore"
        )

        return drop_df

    def create_additional_columns(self, df):
        test_number = re.search(
            "_TEST(\\d*)_",
            self.name
        ).group(1)

        countries = re.search(
            "^\\w+_(\\w+)_01_",
            self.name
        ).group(1)

        df["is_control"] = df["result"].apply(
            lambda value: True if "Control" in value else False
        )

        df["test_id"] = int(test_number)

        df["test_type"] = re.search(
            "_TEST\\d+_(\\w+)_AA",
            self.name
        ).group(1)

        df["countries"] = countries.upper()
        df["target_demographic"] = "Broad"
        df["test_kpi"] = "ITI"

        return df

    @staticmethod
    def rename_columns(df):
        columns_renaming = {
            "creative_concept_name": "creative_name",
            "ci_lower_pct": (
                "result_difference_lower_confidence_interval"
            ),
            "ci_upper_pct": (
                "result_difference_upper_confidence_interval"
            ),
        }

        df_renamed_columns = df.rename(columns=columns_renaming)

        return df_renamed_columns

    @staticmethod
    def sort_columns(df):
        df_sorted = df.loc[:, EXPERIMENTAL_RESULTS_COLUMNS]

        return df_sorted

    def upload_evaluation_to_bq(self, evaluation, destination_table):
        data_is_new, existing_data = self.check_already_existing_data(
            destination_table
        )

        if not data_is_new:
            ExperimentalABTest.handle_existing_data(
                existing_data,
                evaluation
            )

        else:
            ExperimentalABTest.upload_data_to_bq(
                evaluation,
                destination_table
            )

    def check_already_existing_data(self, destination_table):
        existing_data = bigquery_functions.run_query(
            "GET_TEST_RESULTS.sql",
            {
                "PARAM-DESTINATION-TABLE": destination_table,
                "PARAM-CAMPAIGN-NAME": self.name
            }
        )

        return existing_data.empty, existing_data

    @staticmethod
    def handle_existing_data(old_data, new_data):
        print("This campaign already exists in the database")
        print("Existing data:")
        display(old_data)

        print("New data:")
        display(new_data)

        print(
            "Check the data and remove existing records if needed."
        )

    @staticmethod
    def upload_data_to_bq(data, table):
        upload_dataframe_to_bigquery(
            dataframe=data,
            table_id=table,
            project_id="your-gcp-project-id"
        )

        print("Data successfully uploaded.")
