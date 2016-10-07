#!/usr/bin/env python

# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import csv
import time
import uuid

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials

query_template = '''
SELECT
    stn.id,
    stn.name,
    stn.latitude,
    stn.longitude,
    date,
    MAX(prcp) AS prcp,
    MAX(tmin) AS tmin,
    MAX(tmax) AS tmax
FROM
    [bigquery-public-data:ghcn_d.ghcnd_stations] as stn
JOIN
  (SELECT
    id,
    STRING(wx.date) AS date,
    IF (wx.element = 'PRCP', wx.value/10, NULL) AS prcp,
    IF (wx.element = 'TMIN', wx.value/10, NULL) AS tmin,
    IF (wx.element = 'TMAX', wx.value/10, NULL) AS tmax
  FROM
    [bigquery-public-data:ghcn_d.ghcnd_{year}] AS wx
  WHERE
    qflag IS NULL
    AND value IS NOT NULL ) AS wx
ON
  stn.id = wx.id
WHERE
  latitude > -35 AND latitude < -21
  AND longitude > +15 AND longitude < +35
GROUP BY
  stn.id,
  stn.name,
  stn.latitude,
  stn.longitude,
  date
ORDER BY
  date;
'''


def async_query(bigquery,
                project_id,
                query,
                batch=False,
                num_retries=5,
                use_legacy_sql=True):
    job_data = {
        'jobReference': {
            'projectId': project_id,
            'jobId': str(uuid.uuid4())
        },
        'configuration': {
            'query': {
                'query': query,
                'priority': 'BATCH' if batch else 'INTERACTIVE',
                # Set to False to use standard SQL syntax. See:
                # https://cloud.google.com/bigquery/sql-reference/enabling-standard-sql
                'useLegacySql': use_legacy_sql
            }
        }
    }
    return bigquery.jobs().insert(
        projectId=project_id, body=job_data).execute(num_retries=num_retries)


def poll_job(bigquery, job):
    """Waits for a job to complete."""

    print('Waiting for job to finish...')

    request = bigquery.jobs().get(projectId=job['jobReference']['projectId'],
                                  jobId=job['jobReference']['jobId'])

    while True:
        result = request.execute(num_retries=2)

        if result['status']['state'] == 'DONE':
            if 'errorResult' in result['status']:
                raise RuntimeError(result['status']['errorResult'])
            print('Job complete.')
            return

        time.sleep(1)


def main(project_id):
    credentials = GoogleCredentials.get_application_default()
    bigquery = build('bigquery', 'v2', credentials=credentials)

    for year in range(1850, 2016):
        print(year)
        try:
            query_string = query_template.format(year=year)
            query_job = async_query(bigquery, project_id, query_string)

            poll_job(bigquery, query_job)

            page_token = None
            filename = 'sa_weather_{year}.csv'.format(year=year)
            with open(filename, 'wb') as csvfile:
                spamwriter = csv.writer(csvfile)
                while True:
                    page = bigquery.jobs().getQueryResults(
                        pageToken=page_token,
                        **query_job['jobReference']).execute(num_retries=2)

                    for row in page['rows']:
                        spamwriter.writerow([field['v'] for field in row['f']])

                    page_token = page.get('pageToken')
                    if not page_token:
                        break

        except HttpError as err:
            print('Error: {}'.format(err.content))
            raise err


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('project_id', help='Your Google Cloud Project ID.')
    args = parser.parse_args()
    main(args.project_id)
