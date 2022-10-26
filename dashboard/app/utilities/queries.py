from utilities.database_access import Connector
from config import DB_PARAM
import pandas as pd

def get_table_content(table_name, columns=['username']):
    connection = Connector(**DB_PARAM).db_engine
    talent_names = pd.read_sql_table(table_name, connection, columns=columns)
    return talent_names

def get_tweet_dates(vtuber_name):
    connection = Connector(**DB_PARAM).db_engine
    query = '''
        SELECT MIN(dd.date) as min_date, MAX(dd.date) as max_date
        FROM tweet_fact as tf
        JOIN date_dim as dd on tf.date_id = dd.date_id
        JOIN user_dim as ud on ud.user_id = tf.user_id
        WHERE ud.username = %s
    '''
    dates = pd.read_sql_query(
        query, 
        connection,
        params=[vtuber_name]
    )
    return dates

def get_tweet_fact_table(username, date_range):
    connection = Connector(**DB_PARAM).db_engine
    query = '''
        SELECT 
            ROW_NUMBER() OVER(PARTITION BY tf.user_id, tf.date_id) 'row_number',
            tf.retweet_count,
            tf.centrality,
            tf.density,
            tf.avg_clustering_coef,
            tf.reciprocity,
            dd.date
        FROM tweet_fact as tf
        JOIN date_dim as dd on tf.date_id = dd.date_id
        JOIN user_dim as ud on ud.user_id = tf.user_id
        WHERE ud.username = %s 
            and dd.date between %s and %s
    '''
    params = [username, date_range[0], date_range[1]]
    return pd.read_sql(
        query,
        connection,
        params=params
    )