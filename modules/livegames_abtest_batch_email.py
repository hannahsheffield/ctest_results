from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from modules import config, bigquery_functions
from modules.email_sender import EmailBuilder


class BatchResultsEmail:
    def __init__(self, batch_number, email_to):
        self.batch_number = batch_number
        self.email_to = email_to

    def create_email(self, schedule_table, results_table):
        email = EmailBuilder()

        header = self.compose_email_header(schedule_table)
        results = self.get_batch_results(results_table)
        body = self.compose_email_body(results)

        email.html(header).html(body)

        return email

    def compose_email_header(self, schedule_table):
        title = f"Creative Test {self.batch_number} Results"
        batch_metadata = self.get_batch_metadata(schedule_table)

        start_date, end_date = BatchResultsEmail.get_dates(
            batch_metadata
        )

        detailed_results_link = (
            "https://example.com/dashboard"
        )

        header = (
            "<h1>Marketing Analytics</h1>"
            + f"<h2>{title}</h2>"
            + f"Test period: {start_date} - {end_date}<br>"
            + f"More details: {detailed_results_link}<br><br>"
        )

        return header

    def get_batch_metadata(self, schedule_table):
        metadata = bigquery_functions.run_query(
            "GET_BATCH_METADATA.sql",
            {
                "PARAM-SCHEDULE-TABLE": schedule_table,
                "PARAM-TEST-BATCH-NUMBER": str(self.batch_number)
            }
        )

        return metadata

    @staticmethod
    def get_dates(metadata):
        start_date = (
            metadata["start_date"]
            .unique()[0]
            .strftime("%d/%m/%Y")
        )

        end_date = (
            metadata["end_date"]
            .unique()[0]
            .strftime("%d/%m/%Y")
        )

        return start_date, end_date
    
    def get_batch_results(self, results_table):
        results = bigquery_functions.run_query(
            "GET_BATCH_RESULTS.sql",
            {
                "PARAM-RESULTS-TABLE": results_table,
                "PARAM-TEST-BATCH-NUMBER": str(self.batch_number)
            }
        )

        return results

    def compose_email_body(self, results):
        results_summary = BatchResultsEmail.get_results_summary(results)
        results_html_table = BatchResultsEmail.get_results_html_table(results)

        body = results_summary + "<br>" + results_html_table

        return body

    @staticmethod
    def get_results_summary(results):
        num_sig_win = len(
            results.query("result == 'Significant Winner'")
        )

        num_non_sig_win = len(
            results.query("result == 'Non-Significant Winner'")
        )

        num_sig_los = len(
            results.query("result == 'Significant Loser'")
        )

        num_non_sig_los = len(
            results.query("result == 'Non-Significant Loser'")
        )

        summary = (
            f"<b>Number of Significant Winners:</b> {num_sig_win}<br>"
            + f"<b>Number of Non-Significant Winners:</b> {num_non_sig_win}<br>"
            + f"<b>Number of Non-Significant Losers:</b> {num_non_sig_los}<br>"
            + f"<b>Number of Significant Losers:</b> {num_sig_los}<br>"
        )

        return summary

    @staticmethod
    def get_results_html_table(results):
        # creative_name_link is used to make creative_name clickable in the email
        results_links = BatchResultsEmail.create_creative_name_link_col(
            results
        )

        # Separate variants and controls so they can be displayed side by side
        variants = BatchResultsEmail.get_variants(results_links)
        controls = BatchResultsEmail.get_controls(results_links)

        variants_controls = variants.merge(
            controls,
            on="campaign_name",
            how="left"
        )

        variants_controls_sorted = variants_controls.sort_values(
            by="iti_difference",
            ascending=False
        )

        variants_controls_sorted.reset_index(
            inplace=True,
            drop=True
        )

        results_html_table = BatchResultsEmail.filter_cols(
            variants_controls_sorted
        )

        results_html_table_styled = BatchResultsEmail.style_result_labels(
            results_html_table
        )

        return results_html_table_styled

    @staticmethod
    def create_creative_name_link_col(results):
        results["creative_name_link"] = results.apply(
            lambda row: (
                f'<a href="{row["web_view_link"]}">'
                f'{row["creative_name"]}</a>'
            ),
            axis=1
        )

        return results

    @staticmethod
    def get_variants(results):
        variants = results.loc[
            ~results["result"].str.contains("Control"),
            :
        ]

        return variants

    @staticmethod
    def get_controls(results):
        controls_cols = [
            "campaign_name",
            "creative_name_link"
        ]

        controls = (
            results
            .loc[
                results["result"].str.contains("Control"),
                controls_cols
            ]
            .rename(
                columns={
                    "creative_name_link": (
                        "control_creative_name_link"
                    )
                }
            )
        )

        return controls

    @staticmethod
    def filter_cols(results):
        cols = [
            "channel_name",
            "product_name",
            "test_type",
            "creative_name_link",
            "result",
            "iti_difference",
            "control_creative_name_link"
        ]

        results_filtered = results.loc[:, cols]

        return results_filtered

    @staticmethod
    def style_result_labels(results):
        results_styled_step_0 = (
            results
            .style
            .format({"iti_difference": "{:,.2%}".format})
            .map(
                BatchResultsEmail.color_code,
                subset=["result"]
            )
        )

        results_styled = (
            results_styled_step_0
            .set_table_styles([
                {
                    "selector": "thead th",
                    "props": [
                        ("background-color", "#f7f7f9"),
                        ("color", "#333"),
                        ("font-weight", "bold")
                    ]
                },
                {
                    "selector": "tbody td",
                    "props": [
                        ("border", "1px solid #ccc"),
                        ("padding", "8px")
                    ]
                },
                {
                    "selector": "table",
                    "props": [
                        ("border-collapse", "collapse"),
                        ("width", "100%")
                    ]
                },
            ])
        )

        results_styled_html = results_styled.to_html()

        return results_styled_html

    @staticmethod
    def color_code(value):
        color = config.RESULT_COLOR_CODES[value]

        color_property = (
            f"background-color: {color}"
            if value in [
                "Significant Winner",
                "Significant Loser"
            ]
            else f"color: {color}"
        )

        return color_property

    def send_email(self, email):
        email.sendhtml(
            self.email_to,
            f"Creative Test {self.batch_number} Results"
        )
