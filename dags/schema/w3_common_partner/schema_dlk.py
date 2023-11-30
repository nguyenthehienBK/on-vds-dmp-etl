"""
Define table schema for staging
"""
from schema.common.dao_dim import DaoDim
from schema.common.model import BaseModel, FACT_TABLE_TYPE, DIM_TABLE_TYPE
from utils.lakehouse.table_utils import get_content_from_sql_path


class DLKPartnerInfos(DaoDim, BaseModel):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.SCHEMA = [
            {"name": "id", "mode": "NULLABLE", "type": "bigint"},
            {"name": "partner_code", "mode": "NULLABLE", "type": "string"},
            {"name": "partner_name", "mode": "NULLABLE", "type": "string"},
            {"name": "role_type_code", "mode": "NULLABLE", "type": "string"},
            {"name": "is_intermediary", "mode": "NULLABLE", "type": "bit"},
            {"name": "tax_code", "mode": "NULLABLE", "type": "string"},
            {"name": "business_license", "mode": "NULLABLE", "type": "string"},
            {"name": "status", "mode": "NULLABLE", "type": "string"},
            {"name": "description", "mode": "NULLABLE", "type": "string"},
            {"name": "created_at", "mode": "NULLABLE", "type": "timestamp"},
            {"name": "created_by", "mode": "NULLABLE", "type": "bigint"},
            {"name": "updated_at", "mode": "NULLABLE", "type": "timestamp"},
            {"name": "updated_by", "mode": "NULLABLE", "type": "bigint"},
            {"name": "deleted_at", "mode": "NULLABLE", "type": "timestamp"},
            {"name": "deleted_by", "mode": "NULLABLE", "type": "bigint"},
        ]
        self.SCHEMA_RAW = {
            'id': 'int64',
            'partner_code': 'str',
            'partner_name': 'str',
            'role_type_code': 'str',
            'is_intermediary': 'bool',
            'tax_code': 'str',
            'business_license': 'str',
            'status': 'str',
            'description': 'str',
            'created_at': 'datetime64[ns]',
            'created_by': 'int64',
            'updated_at': 'datetime64[ns]',
            'updated_by': 'int64',
            'deleted_at': 'datetime64[ns]',
            'deleted_by': 'int64',
        }

        # self.COLUMNS_SCHEMA = self.DEFAULT_COLUMNS + self.SCHEMA
        self.COLUMNS_SCHEMA = self.SCHEMA
        self.IS_WRITE_TRUNCATE = True
        self.KEY_COLUMNS = [
            {"name": "id", "type": "bigint"}
        ]
        self.TIME_PARTITIONING = None
        self.MIGRATION_TYPE = 'SQL_ID'
        self.TABLE_TYPE = DIM_TABLE_TYPE
        self.EXTRACT = {
            "TIMESTAMP": "",
            "TIMESTAMP_KEY": "",
            "ORDER_BY": "id",
            "JOIN": ""
        }


class DLKServices(DaoDim, BaseModel):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.SCHEMA = [
            {"name": "id", "mode": "NULLABLE", "type": "bigint"},
            {"name": "service_code", "mode": "NULLABLE", "type": "string"},
            {"name": "service_name", "mode": "NULLABLE", "type": "string"},
            {"name": "trans_type_id", "mode": "NULLABLE", "type": "bigint"},
            {"name": "external_service_code", "mode": "NULLABLE", "type": "string"},
            {"name": "description", "mode": "NULLABLE", "type": "string"},
            {"name": "is_financial", "mode": "NULLABLE", "type": "bigint"},
            {"name": "is_internal", "mode": "NULLABLE", "type": "bigint"},
            {"name": "type", "mode": "NULLABLE", "type": "string"},
            {"name": "status", "mode": "NULLABLE", "type": "string"},
            {"name": "created_at", "mode": "NULLABLE", "type": "timestamp"},
            {"name": "created_by", "mode": "NULLABLE", "type": "bigint"},
            {"name": "updated_at", "mode": "NULLABLE", "type": "timestamp"},
            {"name": "updated_by", "mode": "NULLABLE", "type": "bigint"},
            {"name": "deleted_at", "mode": "NULLABLE", "type": "timestamp"},
            {"name": "deleted_by", "mode": "NULLABLE", "type": "bigint"},
        ]
        self.SCHEMA_RAW = {
            'id': 'int64',
            'service_code': 'str',
            'service_name': 'str',
            'trans_type_id': 'int64',
            'external_service_code': 'str',
            'description': 'str',
            'is_financial': 'int64',
            'is_internal': 'int64',
            'type': 'str',
            'status': 'str',
            'created_at': 'datetime64[ns]',
            'created_by': 'int64',
            'updated_at': 'datetime64[ns]',
            'updated_by': 'int64',
            'deleted_at': 'datetime64[ns]',
            'deleted_by': 'int64',
        }

        # self.COLUMNS_SCHEMA = self.DEFAULT_COLUMNS + self.SCHEMA
        self.COLUMNS_SCHEMA = self.SCHEMA
        self.IS_WRITE_TRUNCATE = True
        self.KEY_COLUMNS = [
            {"name": "id", "type": "bigint"}
        ]
        self.TIME_PARTITIONING = None
        self.MIGRATION_TYPE = 'SQL_ID'
        self.TABLE_TYPE = DIM_TABLE_TYPE
        self.EXTRACT = {
            "TIMESTAMP": "",
            "TIMESTAMP_KEY": "",
            "ORDER_BY": "id",
            "JOIN": ""
        }


_ALL = "all"
""" ALL table name in database """

DLK_PARTNER_INFOS = "partner_infos"
DLK_SERVICES = "services"

W3_COMMON_PARTNER_TABLE_SCHEMA = {
    DLK_PARTNER_INFOS: DLKPartnerInfos(DLK_PARTNER_INFOS),
    DLK_SERVICES: DLKServices(DLK_SERVICES),
}

_ALL_DIM = [
    DLK_PARTNER_INFOS,
    DLK_SERVICES
]

_ALL_FACT = [

]

_ALL_TABLE = _ALL_DIM + _ALL_FACT
