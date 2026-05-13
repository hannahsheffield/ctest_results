import numpy as np
from scipy import stats
from modules import config, bigquery_functions, campaign


class ABTest(campaign.Campaign):
    def __init__(self, name, channel_name, start_date, end_date):
        ABTest.handle_invalid_channel_name(channel_name)
        super().__init__(name, channel_name, start_date, end_date)

    @staticmethod
    def handle_invalid_channel_name(channel_name):
        channels = ["network_a", "network_b", "network_c"]
        if channel_name not in channels:
            raise ValueError(
                f"The channel_name provided is not accepted. "
                f"Please select one between: {channels}."
            )
        else:
            pass

    def get_schedule(self, schedule_table):
        schedule = bigquery_functions.run_query(
            "GET_TEST_SCHEDULE.sql",
            {
                "PARAM-CAMPAIGN-NAME": self.name,
                "PARAM-CHANNEL-NAME": self.channel_name,
                "PARAM-START-DATE": self.start_date,
                "PARAM-END-DATE": self.end_date,
                "PARAM-SCHEDULE-TABLE": schedule_table
            }
        )
        return schedule
        
    def get_results(self, schedule, performance):
        performance_clean = ABTest.clean_dataset(performance)
        performance_metrics = ABTest.calculate_metrics(performance_clean)
        statistics = ABTest.calculate_statistics(schedule, performance_metrics)
        results = self.create_results_labels(schedule, statistics)
        return results

    @staticmethod
    def clean_dataset(performance):
        performance_nonulls = performance.loc[
            ~performance["creative_name"].isnull(),
            :
        ]

        performance_nomissing = performance_nonulls.loc[
            performance_nonulls["creative_name"] != "Missing Creative Data",
            :
        ]

        return performance_nomissing
    
    @staticmethod
    def calculate_metrics(performance):
        performance["ctr"] = (
            performance["total_clicks"] /
            performance["total_impressions"]
        )

        performance["cti"] = (
            performance["total_installs"] /
            performance["total_clicks"]
        )

        performance["iti"] = (
            performance["total_installs"] /
            performance["total_impressions"]
        )

        performance["cpi"] = (
            performance["total_cost"] /
            performance["total_installs"]
        )

        performance["it2dr"] = (
            performance["day_2_returners"] /
            performance["total_impressions"]
        )

        performance["iti_error"] = np.sqrt(
            (
                performance["iti"] *
                (1 - performance["iti"])
            ) /
            performance["total_impressions"]
        )

        return performance

    @staticmethod
    def calculate_statistics(schedule, performance):
        control_performance = ABTest.get_control_performance(
            schedule,
            performance
        )

        control_iti = control_performance["iti"].values[0]
        control_iti_error = control_performance["iti_error"].values[0]
        control_it2dr = control_performance["it2dr"].values[0]
        control_total_impressions = (
            control_performance["total_impressions"].values[0]
        )
        
        stat_confidence, stat_confidence_parameter = (
            ABTest.get_stat_confidence(schedule)
        )

        performance["iti_difference"] = (
            (performance["iti"] - control_iti) /
            control_iti
        )

        performance["it2dr_difference"] = (
            (performance["it2dr"] - control_it2dr) /
            control_it2dr
        )
        
        performance = ABTest.calculate_confidence_intervals(
            performance,
            control_iti,
            control_total_impressions,
            stat_confidence_parameter
        )

        performance["z_score"] = (
            (performance["iti"] - control_iti) /
            np.sqrt(
                np.square(performance["iti_error"]) +
                np.square(control_iti_error)
            )
        )

        performance["p_value"] = (
            2 *
            stats.norm.sf(abs(performance["z_score"]))
        )

        return performance

    @staticmethod
    def calculate_confidence_intervals(
        performance,
        control_iti,
        control_impressions,
        confidence_parameter
    ):
        performance = ABTest.calculate_standard_error(
            performance,
            control_iti,
            control_impressions
        )

        performance["ci_lower"] = (
            (performance["iti_difference"] * control_iti) -
            (confidence_parameter * performance["standard_error"])
        )

        performance["ci_upper"] = (
            (performance["iti_difference"] * control_iti) +
            (confidence_parameter * performance["standard_error"])
        )

        performance["ci_lower_pct"] = (
            performance["ci_lower"] /
            control_iti
        )

        performance["ci_upper_pct"] = (
            performance["ci_upper"] /
            control_iti
        )

        return performance

    @staticmethod
    def calculate_standard_error(
        performance,
        control_iti,
        control_impressions
    ):
        performance["standard_error"] = np.sqrt(
            (
                performance["iti"] *
                (1 - performance["iti"])
            ) /
            performance["total_impressions"] +
            (
                control_iti *
                (1 - control_iti)
            ) /
            control_impressions
        )

        return performance

    def create_results_labels(self, schedule, performance):
        control_performance = ABTest.get_control_performance(
            schedule,
            performance
        )

        control_creative_name = (
            control_performance["creative_name"].values[0]
        )

        stat_confidence, _ = ABTest.get_stat_confidence(schedule)
        
        result_conditions = [
            (
                (performance["z_score"] > 0) &
                (performance["p_value"] <= 1 - stat_confidence)
            ),
            (
                (performance["z_score"] > 0) &
                (performance["p_value"] > 1 - stat_confidence)
            ),
            (
                performance["creative_name"] ==
                control_creative_name
            ),
            (
                (performance["z_score"] < 0) &
                (performance["p_value"] > 1 - stat_confidence)
            ),
            (
                (performance["z_score"] < 0) &
                (performance["p_value"] <= 1 - stat_confidence)
            ),
        ]

        result_values = [
            "Significant Winner",
            "Non-Significant Winner",
            "Control " + (
                "network_a"
                if self.channel_name == "network_a"
                else self.channel_name
            ),
            "Non-Significant Loser",
            "Significant Loser"
        ]

        performance["result"] = np.select(
            result_conditions,
            result_values,
            default="N/A"
        )

        return performance

    @staticmethod
    def get_control_performance(schedule, performance):
        control_creative_name = (
            schedule
            .loc[schedule["is_control"] == True, "creative_name"]
            .unique()[0]
        )

        control_performance = performance.loc[
            performance["creative_name"] == control_creative_name
        ]

        return control_performance

    @staticmethod
    def get_stat_confidence(schedule):
        stat_confidence = schedule["stat_confidence"].unique()[0]

        stat_confidence_parameter = (
            config.STATISTICAL_CONFIDENCE_PARAMS[str(stat_confidence)]
        )

        return stat_confidence, stat_confidence_parameter
