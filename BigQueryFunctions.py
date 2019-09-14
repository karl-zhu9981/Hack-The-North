# set up:
from google.cloud import bigquery


class Bigquery_functions:
    def init(self):
        """
        initilizes the service class
        """
        self.client = bigquery.Client()

    def return_nearby_locations(project_id, current_location, table_id):
        """
        Manages queries for bigquery 
        current_location: {latitude: int, longitude: int}
        table_id: model_name
        """
        # Query 1: Changes lat/long into a bigquery geopoint type field
        # collects only necessary fields from provided data. 
        query_1 = '''
        SELECT 
            ST_GEOGPOINT(longitude, latitude) as geopoint,
            recycling institution_name,
            rebate
        FROM {0}.{1}
        '''.format(dataset_id, table_id)
        table_id_cleaned = table_id + '_cleaned'
        create_table_from_query(query_1, dataset_id, table_id_cleaned)

        # query 2 will calculate the distances create an ordered table based on the distance
        query_2 = ''' 
        SELECT * FROM (SELECT 
            ST_distance(geopoint, ST_GEOGPOINT({2}, {3})) as distance
        FROM
            {0}.{1})
        ORDER BY distance ASC
        '''.format(dataset_id, table_id_cleaned,
                   current_location['latitude'], current_location['longitude'])
        final_table_id = table_id + '_processed'
        create_table_from_query(query_2, dataset_id, final_table_id)
        row_iter = convert_table_to_json(dataset_id, final_table_id)
        for row in row_iter:
            pass


def convert_table_to_json(dataset_id, table_id):
    """
    converts a bigquery table to json format table row iterator
    """
    query = '''
    SELECT 
        TO_JSON_STRING(t) AS json
    FROM  
        {0}.{1} AS t; 
    '''.format(dataset_id, table_id)
    # Collect the data as a json
    table_id = '{0}.{1}.{2}'.format(project_id, dataset_id, table_id)
    table = self.client.get_table(table_id)
    return table


def create_table_from_query(query, dataset_id, new_table_id):
    job_config = bigquery.QueryJobConfig()
    table_ref = self.client.dataset(dataset_id).table(new_table_id)
    job_config.destination = table_ref
    query_job = self.client.query(query, location='US', job_config=job_config)
    query_job.result() 
    print('table created: {0}'.format(new_table_id))


if __name__ == '__main__':
    project_id = 'test'
    dataset_id = ''
