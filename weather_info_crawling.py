import requests
import pymysql
from bs4 import BeautifulSoup as bs
from apscheduler.schedulers.background import BackgroundScheduler

 
def main():
    url1 = # NAVER SEARCH URL EX) """https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%B6%80%EC%82%B0+%EA%B0%95%EC%84%9C%EA%B5%AC+%EA%B0%95%EB%8F%99%EB%8F%99+%EB%82%A0%EC%94%A8"""
    url2 = # NAVER SEARCH URL2
    url3 = # NAVER SEARCH URL3
    url_dict = {}
    url_dict[0] = url1
    url_dict[1] = url2
    url_dict[2] = url3
    table_name = # [DB table name1 Ex)"Gangnam", DB table name2, DB table name3]
    with open('login_information.txt', 'rt', encoding='utf8') as f:
        info_list = f.readlines()
        host = info_list[0].strip().split("=")[1]
        port = info_list[1].strip().split("=")[1]
        user = info_list[2].strip().split("=")[1]
        passwd = info_list[3].strip().split("=")[1]
        db = info_list[4].strip().split("=")[1]
        charset = info_list[5].strip().split("=")[1]
        db = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=db, charset=charset)
        cursor = db.cursor()
        for i in range(len(url_dict)):
            url = url_dict[i]
            html = requests.get(url)
            plain_text = html.text
            soup = bs(plain_text, 'lxml')
            area = soup.find('span', {'class': 'btn_select'}).find('em')
            if area is not None:
                area = area.text
            else:
                print("Area is none!")
                area = ""
            current_temp = soup.find('span', {'class': 'todaytemp'})
            if current_temp is not None:
                current_temp = current_temp.text
            else:
                print("Current temp is none!")
                current_temp = -1
            min_temp = soup.find('span', {'class': 'min'})
            if min_temp is not None:
                min_temp = min_temp.text[:-1]
            else:
                print("Min temp is none!")
                min_temp = -1
            max_temp = soup.find('span', {'class': 'max'})
            if max_temp is not None:
                max_temp = max_temp.text[:-1]
            else:
                print("Max temp is none!")
                max_temp = -1
            sensible_temp = soup.find('span', {'class': 'sensible'}).find('em')
            if sensible_temp is not None:
                sensible_temp = sensible_temp.text[:-1]
            else:
                print("Sensible temp is none!")
                sensible_temp = -1
            weather = soup.find('p', {'class': 'cast_txt'})
            if weather is not None:
                weather = weather.text.split(',')[0]
            else:
                print("Weather is none!")
                weather = ""
            uv_num, uv_non_num_content = -1, None
            rainfall_amount = -1
            uv_num = soup.find('span', {'class': 'indicator'}).find('span', {'class': "num"})
            rainfall_html = soup.find('span', {'class': 'rainfall'})
            if uv_num is not None:
                uv_num = uv_num.text
                uv_content = soup.find('span', {'class': 'indicator'}).find('span').text
                uv_non_num_content_point = uv_content.find(uv_num)+len(uv_num)
                uv_non_num_content = uv_content[uv_non_num_content_point: ]
            else:
                print("UV_num is none!")
                uv_num, uv_non_num_content = -1, "null"
            if rainfall_html is not None:
                rainfall_text = rainfall_html.text
                rainfall_amount = rainfall_text.split()[2].split("mm")[0]
            else:
                print("Rainfall_html is none!")
                rainfall_amount = -1
            fine_dust = "null"
            fine_dust_num = -1
            ultra_fine_dust = "null"
            ultra_fine_dust_num = -1
            ozone = "null"
            ozone_num = -1
            dust_list = []
            ozone_text = ""
            for ele in soup.find_all('dd'):
                if "㎍/㎥" in ele.text:
                    dust_list.append(ele.text)
                elif "ppm" in ele.text:
                    ozone_text = ele.text
            if dust_list[0].split("㎍/㎥")[0] is not 'null':
                fine_dust = dust_list[0].split("㎍/㎥")[1]
                fine_dust_num = dust_list[0].split("㎍/㎥")[0]
            else:
                print("Fine dust is none!")
            if dust_list[1].split("㎍/㎥")[0] is not 'null':
                ultra_fine_dust = dust_list[1].split("㎍/㎥")[1]
                ultra_fine_dust_num = dust_list[1].split("㎍/㎥")[0]
            else:
                print("Ultra fine dust is none!")
            if ozone_text.split("ppm")[1] is not '':
                ozone = ozone_text.split("ppm")[1]
                ozone_num = ozone_text.split("ppm")[0]
            else:
                print("Ozone is none!")
            p_rainfall = soup.find("div", {'class': 'info_list rainfall _tabContent'})
            if p_rainfall is not None:
                p_rainfall = p_rainfall.text.strip().split()[2][:-1]
            else:
                print("P_rainfall is none!")
                p_rainfall = -1
            wind_speed = soup.find("div", {'class': 'info_list wind _tabContent'})
            if wind_speed is not None:
                wind_speed = wind_speed.text.strip().split()[2][:-3]
            else:
                print("Wind speed is none!")
                wind_speed = -1
            humidity = soup.find("div", {'class': 'info_list humidity _tabContent'})
            if humidity is not None:
                humidity = humidity.text.strip().split()[2][:-1]
            else:
                print("Humidity is none!")
                humidity = -1
            try:
                float(current_temp)
            except Exception:
                print(area, "current temp..", current_temp)
                current_temp = -1.0
            try:
                float(min_temp)
            except Exception:
                print(area, "min_temp..", min_temp)
                min_temp = -1.0
            try:
                float(max_temp)
            except Exception:
                print(area, "max_temp..", max_temp)
                max_temp = -1.0
            try:
                float(sensible_temp)
            except Exception:
                print(area, "sensible_temp..", sensible_temp)
                sensible_temp = -1.0
            try:
                float(uv_num)
            except Exception:
                print(area, "uv_num..", uv_num)
                uv_num = -1.0
            try:
                float(rainfall_amount)
            except Exception:
                print(area, "rainfall_amount..", rainfall_amount)
                rainfall_amount = -1.0
            try:
                float(fine_dust_num)
            except Exception:
                print(area, "fine_dust_num..", fine_dust_num)
                fine_dust_num = -1.0
            try:
                float(ultra_fine_dust_num)
            except Exception:
                print(area, "ultra_fine_dust_num..", ultra_fine_dust_num)
                ultra_fine_dust_num = -1.0
            try:
                float(ozone_num)
            except Exception:
                print(area, "ozone_num..", ozone_num)
                ozone_num = -1.0
            try:
                float(p_rainfall)
            except Exception:
                print(area, "p_rainfall..", p_rainfall)
                p_rainfall = -1.0
            try:
                float(wind_speed)
            except Exception:
                print(area, "wind_speed..", wind_speed)
                wind_speed = -1.0
            try:
                float(humidity)
            except Exception:
                print(area, "humidity..", humidity)
                humidity = -1.0
            sql = """
                INSERT INTO {18}
                (m_date, area, current_temp, min_temp, max_temp, sensible_temp, weather, uv_num, uv_non_num_content,
                rainfall_amount, find_dust_num, find_dust, ultra_find_dust_num, ultra_find_dust, 
                ozone_num, ozone, p_rainfall, wind_speed, humidity)
                VALUES(now(), "{0}", {1}, {2}, {3}, {4}, "{5}", {6}, "{7}", {8}, {9}, "{10}", {11}, "{12}", {13}, "{14}", {15}, {16}, {17});
                  """.format(area, float(current_temp), float(min_temp), float(max_temp), float(sensible_temp), weather, float(uv_num), uv_non_num_content,
                float(rainfall_amount), float(fine_dust_num), fine_dust, float(ultra_fine_dust_num), ultra_fine_dust, 
                float(ozone_num), ozone, float(p_rainfall), float(wind_speed), float(humidity), table_name[i])
            cursor.execute(sql)
        db.commit()
        db.close()
        print("done")
        
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(main, 'interval', minutes=15, start_date="2019-09-22 15:15:00")
    scheduler.start()
