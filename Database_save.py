from Database_login import LoginInformation
from Crawaling_information import WeatherInformationCralwer
from apscheduler.schedulers.background import BackgroundScheduler
import pymysql
import time
import sys


class DatabaseSave:
    def __init__(self):
        self._db = None
        
             
    def _set_db(self, database):
        if database is None:
            print("Connection method of pymysql object returns none. Please check.")
            sys.exit(0)
        self._db = database
    
    
    def main(self):
        self._db_connect()
        self._save_data()
        
     
    def _db_connect(self):
        _login = LoginInformation()
        _login.main()
        _host = _login.host
        _user = _login.user
        _port = int(_login.port)
        _passwd = _login.password
        _db = _login.db_name
        _charset = _login.charset
        _db = pymysql.connect(host=_host, port=_port, user=_user,
                               passwd=_passwd, db=_db, charset=_charset)
        self._set_db(_db)
        
        
    def _save_data(self):
        def _get_table_name():
            try:
                with open('./db_table_name_information.txt', 'rt', encoding='utf8') as file:
                    _table_name_dict = {}
                    for row in file.readlines():
                        key = row.split("=")[0].strip()
                        value = row.split("=")[1].strip()
                        if len(key) == 0 or len(value) == 0:
                            raise AttributeError
                        _table_name_dict[key] = value
                return _table_name_dict
            except FileNotFoundError as e:
                print("The file containing table name information doesn't exist in the same path. Please check.")
                sys.exit(0)
            except AttributeError as e:
                print("Some information in the table_name information file are missing. Please check.")
                sys.exit(0)
                
        def _convert_into_valid_form(value_dict):
            for area in value_dict.keys():
                for i, (key, value) in enumerate(value_dict[area].items()):
                    if value is None:
                        if i in [0, 1, 2, 3, 5, 6, 7, 8, 9, 12, 14, 16]:
                            value_dict[area][key] = 'NULL'
                        else:
                            value_dict[area][key] = ''
                        continue
                    try:
                        value_dict[area][key] = float(value)
                    except ValueError as e:
                        continue
            return value_dict
                
        _weather_info = WeatherInformationCralwer()
        _weather_info.main()    
        _table_dict = _get_table_name()
        _data_dict = _convert_into_valid_form(_weather_info.data_dict)
        for area, table in _table_dict.items():
            for region, data in _data_dict.items():
                if region.split()[2] == area:
                    _sql = f"""
                            INSERT INTO {table}
                            (m_date, area, current_temp, min_temp, max_temp, sensible_temp, 
                            weather, uv_num, uv_non_num_content, rainfall_amount, find_dust_num, 
                            find_dust, ultra_find_dust_num, ultra_find_dust, 
                            ozone_num, ozone, p_rainfall, wind_speed, humidity)
                            VALUES(now(), "{region}", {_data_dict[region]['current_temp']}, 
                            {_data_dict[region]['min_temp']}, {_data_dict[region]['max_temp']}, 
                            {_data_dict[region]['sensible_temp']}, "{_data_dict[region]['weather']}", 
                            {_data_dict[region]['uv_num']}, "{_data_dict[region]['uv_non_num_content']}", 
                            {_data_dict[region]['rainfall_amount']}, {_data_dict[region]['fine_dust_num']}, 
                            "{_data_dict[region]['fine_dust']}", {_data_dict[region]['ultra_fine_dust_num']}, 
                            "{_data_dict[region]['ultra_fine_dust']}", {_data_dict[region]['ozone_num']}, 
                            "{_data_dict[region]['ozone']}", {_data_dict[region]['p_rainfall']}, 
                            {_data_dict[region]['wind_speed']}, {_data_dict[region]['humidity']});
                           """
                    _cursor = self._db.cursor()
                    _cursor.execute(_sql)
        self._db.commit()
        self._db.close()
        print("done")
                    
                
if __name__ == "__main__":
    save = DatabaseSave()
    scheduler = BackgroundScheduler()
    scheduler.add_job(save.main, 'interval', minutes=15, start_date="2020-06-13 12:00:00")
    scheduler.start()
    while True:
        time.sleep(0.3)
