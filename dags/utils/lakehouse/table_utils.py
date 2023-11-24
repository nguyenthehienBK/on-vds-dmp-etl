import datetime
from dateutil.relativedelta import relativedelta
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook
# from dags.schema.generic.schema_dlk import _TABLE_SCHEMA as generic_tbl
# from dags.schema.lakehouse_template.schema_dlk import _TABLE_SCHEMA as lakehouse_tbl


# def get_all_database_table(db_source):
#     if db_source == "template":
#         return lakehouse_tbl
#     if db_source == "generic":
#         return generic_tbl
def get_hdfs_path(
        table_name: str = None,
        hdfs_conn_id: str = None,
        layer: str = None,
        bucket: str = None,
        business_day: str = "19700101",
) -> str:
    conn = BaseHook.get_connection(hdfs_conn_id)
    host = conn.host
    port = str(conn.port)
    # host = 'host_test'
    # port = 'post_test'
    if table_name is None:
        return ""
    if layer == "RAW":
        return f"hdfs://{host}:{port}/{bucket}/{layer}/{table_name}/{business_day}/"
    else:
        return f"hdfs://{host}:{port}/{bucket}/{layer}/{table_name}/"


def get_content_from_sql_path(sql_path: str) -> str:
    data = ''
    try:
        with open(sql_path, 'r') as file:
            data = file.read()
    except:
        print(f'Loi doc file sql {sql_path}')
    return data


# from schema.lakehouse_template.schema_dlk import (
#     get_table_info as dlk_info,
#     valid_tables as dlk_valid_tables,
#     valid_all_tables as dlk_valid_all_tables,
#     get_columns,
#     get_sql,
#     is_fact_table as dlk_is_fact_table,
# )
# from schema.lakehouse_template.schema_dwh import (
#     get_table_info as dwh_info,
#     valid_tables as dwh_valid_tables,
#     valid_all_tables as dwh_valid_all_tables,
#     is_fact_table as dwh_is_fact_table,
# )
from utils.database.db_data_type import UpsertType

PAGING = 100000
MAXIMUM_FILE_LOAD_GCS2BQ = 10000


def get_etl_time():
    etl_time = Variable.get("kv_etl_time", default_var={}, deserialize_json=True)
    from_date = etl_time.get("from")
    to_date = etl_time.get("to")
    if not from_date:
        from_date = (datetime.datetime.now() - relativedelta(days=1)).strftime(
            "%Y-%m-%d"
        )
    if not to_date:
        to_date = (datetime.datetime.now() - relativedelta(days=1)).strftime("%Y-%m-%d")
    return from_date, to_date


# def table_info_factory(table_name, is_dlk=False, only_schema=False):
#     if is_dlk:
#         return dlk_info(table_name=table_name, only_schema=only_schema)
#     return dwh_info(table_name=table_name, only_schema=only_schema)


# def valid_all_tables_factory(ls_tbl, is_dlk=False):
#     if is_dlk:
#         return dlk_valid_all_tables(ls_tbl=ls_tbl)
#     return dwh_valid_all_tables(ls_tbl=ls_tbl)
#
#
# def is_fact_table_factory(table_name, is_dlk=False):
#     if is_dlk:
#         return dlk_is_fact_table(table_name=table_name)
#     return dwh_is_fact_table(table_name=table_name)


"""
File path:
- Dim: dimensions_table/Branch/*.parquet AND dimensions_table/Branch/2019-08-26/*.parquet
- Facts: facts_table/2019-08-26/share_prod_105/*.parquet
fact_path = "FACTS_TABLE/extract_date_str/SHARE_PROD_FORMAT/table_name.parquet"
dimension_path = "DIMENSIONS_TABLE/table_name/server_key__table_name__paging__file_idx.parquet"

"""

# FACTS_TABLE = 'facts_table'
# DIMENSIONS_TABLE = 'dimensions_table'
FIXED_TABLE = "fixed_table"
CREATE_NEVER = "CREATE_NEVER"
CREATE_IF_NEEDED = "CREATE_IF_NEEDED"
WRITE_TRUNCATE = "WRITE_TRUNCATE"
WRITE_APPEND = "WRITE_APPEND"
WRITE_EMPTY = "WRITE_EMPTY"

# BLOB_NAME_DIM = "{}/{}/{}.parquet"
# BLOB_NAME_FACTS = "{}/{}/{}/{}.parquet"
# SHARE_PROD_FORMAT = "share_prod_"


"""
File path:
- Dim: dimensions_table/kv_mssql/2019-08-26/shard_105/Branch/Branch_*.parquet
- Facts: facts_table/kv_mssql/2019-08-26/shard_105/Invoice/Invoice_*.parquet
"""


# def extract_table_info(
#         db_source, table_name, is_fact=False, etl_from=None, etl_to=None, hdfs_conn_id=None,
#         layer=None, business_day="19700101"
# ):
#     return {
#         "sql": get_sql(
#             table_name=table_name,
#             etl_from=etl_from,
#             etl_to=etl_to,
#             is_fact=is_fact,
#         ),
#         "filename": get_hdfs_path(
#             table_name=table_name,
#             hdfs_conn_id=hdfs_conn_id,
#             layer=layer,
#             bucket=db_source,
#             business_day=business_day,
#         ),
#         "schema": table_info_factory(
#             table_name=table_name, is_dlk=True, only_schema=True
#         ),
#     }


def get_partition_column_expr(table, alias_table=None):
    if hasattr(table, "TIME_PARTITIONING") and table.TIME_PARTITIONING:
        partition = table.TIME_PARTITIONING
        field_type = partition["type"].upper()
        if alias_table:
            field = f'{alias_table}.`{partition["field"]}`'
        else:
            field = f'`{partition["field"]}`'

        if field_type == UpsertType.DAY:
            partition_colum_expr = f"date({field})"
        elif field_type == UpsertType.NONE:
            partition_colum_expr = field
        else:
            partition_colum_expr = f"{field_type}({field})"

        return partition_colum_expr
    else:
        return None


class ExtractSQL:
    SQL_TEMPLATE_DIM = "dags/sql/template/extract_sql_template_dim.sql"
    SQL_TEMPLATE_FACT = "dags/sql/template/extract_sql_template_facts.sql"
    EQUAL_FORMAT = "WHERE {} = '{}'"
    BETWEEN_FORMAT = "WHERE {} BETWEEN '{}' AND '{}'"

def get_sql_param(tbl):
    where_condition = ""
    timestamp = ""
    join = ""
    order_by = ""
    ext_columns = ""
    timestamp_key = ""
    sql_source_file = False

    table_name = tbl.TABLE_NAME
    prefix = table_name
    timestamp = tbl.EXTRACT["TIMESTAMP"]
    join = tbl.EXTRACT["JOIN"]
    order_by = tbl.EXTRACT["ORDER_BY"]
    timestamp_key = tbl.EXTRACT["TIMESTAMP_KEY"]
    ls_columns = [s["name"] for s in tbl.SCHEMA]
    columns = ''
    for col in ls_columns:
        columns = columns + col + '\n'

    sql_val = {
        "columns": columns,
        "table_name": prefix,
        "where_condition": where_condition,
        "timestamp": timestamp,
        "join": join,
        "order_by": order_by,
    }
    if tbl.TABLE_TYPE == "DIM":
        sql_file = ExtractSQL.SQL_TEMPLATE_DIM
    else:
        sql_file = ExtractSQL.SQL_TEMPLATE_FACT
    query = get_content_from_sql_path(sql_file)

    return {
        "file": sql_file,
        "query": query,
        "timestamp_key": timestamp_key,
        "params": sql_val,
        "sql_source_file": sql_source_file
    }
