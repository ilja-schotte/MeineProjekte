


import yaml
import MetisTools




with open('db_config.yaml', 'r', encoding="utf-8") as fp_config:
    config = yaml.safe_load(fp_config)

db_conn_string_raw = config.get("MIRAKEL").get("db_connection_string_raw")
db_name = config.get("MIRAKEL").get("db_name")
db_port = config.get("MIRAKEL").get("db_port")
db_user = config.get("MIRAKEL").get("db_user")
db_pwd = config.get("MIRAKEL").get("db_pwd")
db_hostname = config.get("MIRAKEL").get("db_hostname")
db_hostname_alt = config.get("MIRAKEL").get("db_hostname_alt")
db_service = config.get("MIRAKEL").get("db_service")
db_arraysize = config.get("MIRAKEL").get("db_arraysize")

sql = """select table_name as "Tabellenname" 
from all_tables
WHERE table_name LIKE '%WERTE%'"""

with MetisTools.DBConnector(
    db_name=db_name,
    db_hostname=db_hostname,
    db_hostname_alt=db_hostname_alt,
    db_service=db_service,
    db_port=db_port,
    db_user=db_user,
    db_pwd=db_pwd,
    db_conn_string_raw=db_conn_string_raw,
    db_arraysize=db_arraysize) as db:

    result = db.request(sql=sql)
    print(result)
    