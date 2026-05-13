from bquer import BQuer
from modules import config

BQ_PROJECT_NAME = config.BQ_BILLING_PROJECT_ID
bqCreator = BQuer.create_with_project(project=BQ_PROJECT_NAME)

def run_query(query_file, params=None):
    query = get_query(query_file)
    if params:
        query = replace_query_params(query, params)
    response = execute_query(query)
    return response

def get_query(query_file):
    with open(f"queries/{query_file}", "r") as queryFile:
        query = queryFile.read()
    return query

def replace_query_params(query, params):
    for key, value in params.items():
        query = query.replace(key, str(value))
    return query

def execute_query(query):
    response = bqCreator.query(
        query,
        dry_run=False,
        block=True
        )
    return response
