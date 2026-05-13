{
  "cells": [
    {
      "cell_type": "markdown",
      "id": "project-title",
      "metadata": {},
      "source": [
        "# Creative Test Results - Single Campaign Evaluation\n",
        "\n",
        "This notebook evaluates one creative A/B test campaign, calculates statistical results, formats the output, and optionally uploads the results to a BigQuery table."
      ]
    },
    {
      "cell_type": "markdown",
      "id": "libraries-heading",
      "metadata": {},
      "source": [
        "## Libraries"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "imports",
      "metadata": {},
      "outputs": [],
      "source": [
        "from datetime import datetime, timedelta\n",
        "\n",
        "import pandas as pd\n",
        "\n",
        "from modules import production_ab_test, experimental_ab_test\n",
        "\n",
        "pd.set_option(\"display.max_columns\", None)\n",
        "pd.set_option(\"display.max_colwidth\", None)\n",
        "pd.set_option(\"display.max_rows\", 100)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "evaluation-heading",
      "metadata": {},
      "source": [
        "## Evaluation"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "config",
      "metadata": {
        "tags": []
      },
      "outputs": [],
      "source": [
        "CAMPAIGN_NAME = \"campaign_name\"\n",
        "CHANNEL_NAME = \"network_a\"\n",
        "START_DATE = \"YYYY-MM-DD\"\n",
        "END_DATE = \"YYYY-MM-DD\"\n",
        "SCHEDULE_TABLE = \"project.dataset.schedule_table\"\n",
        "RESULTS_TABLE = \"project.dataset.results_table\"\n",
        "\n",
        "abtest = production_ab_test.ProductionABTest(\n",
        "    name=CAMPAIGN_NAME,\n",
        "    channel_name=CHANNEL_NAME,\n",
        "    start_date=START_DATE,\n",
        "    end_date=END_DATE\n",
        ")"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "workflow-heading",
      "metadata": {},
      "source": [
        "## Run evaluation workflow\n",
        "\n",
        "The workflow retrieves the test schedule, pulls campaign performance, calculates A/B test statistics, and formats the results for reporting."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "run-evaluation",
      "metadata": {},
      "outputs": [],
      "source": [
        "schedule = abtest.get_schedule(SCHEDULE_TABLE)\n",
        "performance = abtest.get_performance()\n",
        "\n",
        "results = abtest.get_results(schedule, performance)\n",
        "formatted_results = abtest.format_results(schedule, results)\n",
        "\n",
        "formatted_results.head()"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "upload-heading",
      "metadata": {},
      "source": [
        "## BigQuery upload\n",
        "\n",
        "The upload step checks for existing results before writing new rows to the destination table."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "id": "upload-results",
      "metadata": {
        "tags": []
      },
      "outputs": [],
      "source": [
        "abtest.upload_results_to_bq(\n",
        "    formatted_results,\n",
        "    RESULTS_TABLE\n",
        ")"
      ]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.11.10"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
