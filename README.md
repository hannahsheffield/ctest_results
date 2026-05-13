<a name="readme-top"></a>

<div align="center">

  <h1>Creative A/B Test Results Pipeline</h1>

  <p>
    <strong>An  Python, SQL, and BigQuery project for calculating, formatting, uploading, and emailing creative A/B test results.</strong>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
    <img src="https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white" />
    <img src="https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=googlecloud&logoColor=white" />
    <img src="https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  </p>

</div>

---

## Overview

Creative A/B Test Results Pipeline is an analytics engineering project that calculates statistical results for creative tests across marketing campaigns.

The project pulls campaign performance data, compares creative variants against a control, calculates key performance metrics, applies statistical significance testing, formats the output for reporting, prevents duplicate uploads, and generates summary emails for stakeholders.

> This is a portfolio-safe version of a workplace automation project. It uses generic names, placeholder table references, mock campaign names, and anonymised business logic. No proprietary data, internal URLs, credentials, or confidential company logic are included.

---

## Problem

Creative test results can be difficult to process manually when campaigns run across multiple networks and reporting formats.

Common issues include:

<ul>
  <li>Performance data coming from different source tables</li>
  <li>Different networks requiring different query logic</li>
  <li>Manual calculation of creative test metrics</li>
  <li>Inconsistent winner / loser labelling</li>
  <li>Duplicate result uploads</li>
  <li>Manual stakeholder updates</li>
  <li>Campaigns failing silently during batch processing</li>
</ul>

This project solves those issues by creating a reusable results pipeline.

---

## Solution

The pipeline automates the end-to-end creative test results workflow:

<ol>
  <li>Pulls test schedule data from BigQuery</li>
  <li>Pulls campaign performance data by network type</li>
  <li>Cleans missing or invalid creative data</li>
  <li>Calculates test metrics such as CTR, CTI, ITI, CPI, and day 2 return rate</li>
  <li>Compares each creative against the control</li>
  <li>Calculates confidence intervals, z-scores, and p-values</li>
  <li>Labels creatives as winners, losers, or controls</li>
  <li>Formats results into reporting-ready tables</li>
  <li>Checks for existing results before uploading</li>
  <li>Processes batches of campaigns</li>
  <li>Creates an HTML summary email for stakeholders</li>
</ol>

---

## Tech Stack

<table>
  <tr>
    <th>Tool</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>Python</td>
    <td>Main pipeline logic and class-based workflow</td>
  </tr>
  <tr>
    <td>Pandas</td>
    <td>Data cleaning, formatting, merging, and output preparation</td>
  </tr>
  <tr>
    <td>NumPy</td>
    <td>Metric calculations and conditional result labelling</td>
  </tr>
  <tr>
    <td>SciPy</td>
    <td>Statistical significance testing using normal distribution calculations</td>
  </tr>
  <tr>
    <td>BigQuery</td>
    <td>Schedule retrieval, performance extraction, and result storage</td>
  </tr>
  <tr>
    <td>SQL</td>
    <td>Campaign performance queries and result lookups</td>
  </tr>
  <tr>
    <td>Jupyter Notebooks</td>
    <td>Manual campaign and batch execution workflows</td>
  </tr>
  <tr>
    <td>HTML Email</td>
    <td>Stakeholder result summaries</td>
  </tr>
</table>

---

## Key Features

<table>
  <tr>
    <th>Feature</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><strong>A/B test result engine</strong></td>
    <td>Calculates performance metrics, statistical differences, confidence intervals, p-values, and result labels.</td>
  </tr>
  <tr>
    <td><strong>Campaign abstraction</strong></td>
    <td>Uses a base campaign class to pull performance data from different network-specific sources.</td>
  </tr>
  <tr>
    <td><strong>Production test formatting</strong></td>
    <td>Formats results into a standard schema for reporting and BigQuery upload.</td>
  </tr>
  <tr>
    <td><strong>Batch processing</strong></td>
    <td>Processes multiple campaigns in one workflow and separates successful results from issues requiring review.</td>
  </tr>
  <tr>
    <td><strong>Duplicate upload prevention</strong></td>
    <td>Checks whether results already exist before uploading new records.</td>
  </tr>
  <tr>
    <td><strong>HTML summary emails</strong></td>
    <td>Creates stakeholder-friendly result summaries with counts, links, and formatted tables.</td>
  </tr>
  <tr>
    <td><strong>Test coverage</strong></td>
    <td>Includes pytest examples for schedule retrieval, campaign performance pulls, and result labelling.</td>
  </tr>
</table>

---

## Metrics Calculated

<table>
  <tr>
    <th>Metric</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>ctr</code></td>
    <td>Click-through rate: clicks divided by impressions</td>
  </tr>
  <tr>
    <td><code>cti</code></td>
    <td>Click-to-install rate: installs divided by clicks</td>
  </tr>
  <tr>
    <td><code>iti</code></td>
    <td>Impression-to-install rate: installs divided by impressions</td>
  </tr>
  <tr>
    <td><code>cpi</code></td>
    <td>Cost per install: total cost divided by installs</td>
  </tr>
  <tr>
    <td><code>it2dr</code></td>
    <td>Impression-to-day-2-returner rate</td>
  </tr>
  <tr>
    <td><code>iti_difference</code></td>
    <td>Relative ITI difference versus the control creative</td>
  </tr>
  <tr>
    <td><code>p_value</code></td>
    <td>Statistical probability used to determine significance</td>
  </tr>
  <tr>
    <td><code>z_score</code></td>
    <td>Standardised difference between variant and control performance</td>
  </tr>
</table>

---

## Result Labels

<table>
  <tr>
    <th>Result Label</th>
    <th>Meaning</th>
  </tr>
  <tr>
    <td><strong>Significant Winner</strong></td>
    <td>The creative outperformed the control and passed the statistical significance threshold.</td>
  </tr>
  <tr>
    <td><strong>Non-Significant Winner</strong></td>
    <td>The creative outperformed the control, but not strongly enough to be statistically significant.</td>
  </tr>
  <tr>
    <td><strong>Control</strong></td>
    <td>The baseline creative used for comparison.</td>
  </tr>
  <tr>
    <td><strong>Non-Significant Loser</strong></td>
    <td>The creative underperformed the control, but not strongly enough to be statistically significant.</td>
  </tr>
  <tr>
    <td><strong>Significant Loser</strong></td>
    <td>The creative underperformed the control and passed the statistical significance threshold.</td>
  </tr>
</table>

---

## Statistical Methodology

The pipeline compares each creative variant against the control creative using impression-to-install rate.

```text
ITI = total_installs / total_impressions
