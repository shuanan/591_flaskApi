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

def getSection(region):
    try:
        #region = request["region"]

        conn = pymysql.connect(**db_settings)
	
        with conn.cursor() as cursor:
            sql = """SELECT name, value FROM tbl_urlcondition
                    where kind = %s and subKind = %s
                    """
            val = ("section", region)
            cursor.execute(sql, val)
            result = cursor.fetchall()

            areas_list = []
            for r in result:
                area_dict=dict()
                area_dict["name"] = r[0]
                area_dict["value"] = r[1]   
                areas_list.append(area_dict)

            status ="success"
            if len(result) == 0 :
                status = "error"

            result = {
                "status":status,
                "data": areas_list
                }
            return result

    except Exception as ex:
        print(ex)

def getRegion(self):
    try:
        conn = pymysql.connect(**db_settings)
		
        with conn.cursor() as cursor:
            sql = """SELECT name, value FROM tbl_urlcondition
                    where kind = %s 
                    """
            val = ("region")
            cursor.execute(sql, val)
            result = cursor.fetchall()

            areas_list = []
            for r in result:
                area_dict=dict()
                area_dict["name"] = r[0]
                area_dict["value"] = r[1]   
                areas_list.append(area_dict)

            status ="success"
            if len(result) == 0 :
                status = "error"

            result = {
                "status":status,
                "data": areas_list
                }
            return result

    except Exception as ex:
        print(ex)


