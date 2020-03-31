from google.cloud import bigquery


with open('country.sql', 'r') as myfile:
    sql = myfile.read()

# Construct a BigQuery client object.
client = bigquery.Client()
query_job = client.query(sql)  # Make an API request.

print("Country update job: {}".format(query_job.job_id))
