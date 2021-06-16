from decouple import config
import pymysql
import time

db_settings = {
        "host": config("MYSQL_HOST"),
        "port": 3306,
        "user": config("MYSQL_USER"),
        "password": config("MYSQL_PWD"),
        "db": config("MYSQL_DB"),
        "charset": "utf8"
    }

def getSection(request):
    try:
        region = request["region"]

        conn = pymysql.connect(**db_settings)
		
        with conn.cursor() as cursor:
            sql = """SELECT name, value FROM tbl_urlcondition
                    where kind = %s and subKind = %s
                    """
            val = ("section", region)
            cursor.execute(sql, val)
            result = cursor.fetchall()

            status ="success"
            if len(result) == 0 :
                status = "error"

            result = {
                "status":status,
                "data": result
                }
            return result

    except Exception as ex:
        print(ex)

