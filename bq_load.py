from google.cloud import bigquery
client = bigquery.Client()
filename = 'data.csv'
dataset_id = 'covid19'
table_id = 'daily_reports'

dataset_ref = client.dataset(dataset_id)
table_ref = dataset_ref.table(table_id)
job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 0
job_config.autodetect = False
job_config.write_disposition = 'WRITE_TRUNCATE'

with open(filename, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

job.result()  # Waits for table load to complete.

print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))
