import requests
import sys
from bs4 import BeautifulSoup as bs


class WeatherInformationCralwer:
    def __init__(self):
        self._url_dict = {}
        self._soup_inst_dict = {}
        self._data_dict = {}
        
        
    @property
    def data_dict(self):
        if len(self._data_dict) == 0:
            print("Crawled value dictionary is empty. Please check.")
            sys.exit(0)
        return self._data_dict 
    
        
    def _set_url_dict(self, url_info):
        for url in url_info:
            key = url.strip().split("@")[0]
            value = url.strip().split("@")[1]
            if len(value) != 0:
                self._url_dict[key] = value
                
                
    def _set__soup_inst_dict(self):
        self._soup_inst_dict["current_temp"] = "global current_temp; current_temp = None; " \
                                               "current_temp = soup.find('span', {'class': 'todaytemp'}).text"
        self._soup_inst_dict["min_temp"] = "global min_temp; min_temp = None; " \
                                           "min_temp = soup.find('span', {'class': 'min'}).text[:-1]"
        self._soup_inst_dict["max_temp"] = "global max_temp; max_temp = None; " \
                                           "max_temp = soup.find('span', {'class': 'max'}).text[:-1]"
        self._soup_inst_dict["sensible_temp"] = "global sensible_temp; sensible_temp = None; " \
                                                "sensible_temp = soup.find('span', {'class': 'sensible'})" \
                                                ".find('em').text[:-1]"
        self._soup_inst_dict["weather"] = "global weather; weather = None; " \
                                          "weather = soup.find('p', {'class': 'cast_txt'}).text.split(',')[0]"
        self._soup_inst_dict["rainfall_amount"] = "global rainfall_amount; rainfall_amount = None; " \
                                   "rainfall_amount = soup.find('span', " \
                                   "{'class': 'rainfall'}).text.split()[2].split('mm')[0]" 
        self._soup_inst_dict["p_rainfall"] = "global p_rainfall; p_rainfall = None; " \
                                   "p_rainfall = soup.find('div', " \
                                   "{'class': 'info_list rainfall _tabContent'}).text.strip().split()[2][:-1]" 
        self._soup_inst_dict["wind_speed"] = "global wind_speed; wind_speed = None; " \
                                   "wind_speed = soup.find('div', " \
                                   "{'class': 'info_list wind _tabContent'}).text.strip().split()[2][:-3]"
        self._soup_inst_dict["humidity"] = "global humidity; humidity = None; " \
                                   "humidity = soup.find('div', " \
                                   "{'class': 'info_list humidity _tabContent'}).text.strip().split()[2][:-1]"
        
        
    def main(self):
        self._information_crawler()
    
    
    def _information_crawler(self):
        self._read_url()
        self._information_crawling()
    
    
    def _read_url(self):
        def _check_information_file_validation(_info):
            if len(_info) == 0:
                print("URL information file is empty. Please check.")
                sys.exit(0)
            _valid_count = 0
            for url in _info:
                value = url.strip().split("@")[1]
                if len(value) != 0:
                    _valid_count += 1
            if _valid_count == 0 :
                print("There is no url in the file. Please check.")
                sys.exit(0)
         
        try:
            _url_file =  open('./url_information.txt', 'rt', encoding='utf8')
        except FileNotFoundError as e:
            print("The file containing url information doesn't exist in the same path. Please check.")
            sys.exit(0)
        _url_information = _url_file.readlines()
        _check_information_file_validation(_url_information)
        self._set_url_dict(_url_information)
        
        
    def _information_crawling(self):
        def _filter_none_information(instruction, soup):
            try:
                exec(instruction)
            except Exception:
                raise AttributeError
                    
        _crawled_value_dict = {}    
        url_dict = self._url_dict   
        for key, value in url_dict.items():
            url = url_dict[key]
            html = requests.get(url)
            plain_text = html.text   
            soup = bs(plain_text, 'lxml')
            self._set__soup_inst_dict()
            area = soup.find('span', {'class': 'btn_select'}).find('em').text
            for name, inst in self._soup_inst_dict.items():
                try:
                    _filter_none_information(inst, soup)
                except AttributeError as e:
                    print(f"{name} information of {area} is none.")
                    _crawled_value_dict[name] = None
                else:
                    _crawled_value_dict[name] = eval(name) 
            _crawled_value_dict["uv_num"], _crawled_value_dict["uv_non_num_content"] = \
                                                    self._get_uv_information(area, soup)
            for key, value in self._get_dust_and_ozone_information(area, soup).items():
                _crawled_value_dict[key] = value
            self._data_dict[area] = _crawled_value_dict
            
            

    def _get_uv_information(self, region, soup):
        try:
            _uv_content = soup.find('span', {'class': 'indicator'}).find('span').text
        except AttributeError:
            print(f"UV information of {region} is none.")
            return (None, None)
        try:
            _uv_num = soup.find('span', {'class': 'indicator'}).find('span', {'class': "num"}).text
        except AttributeError:
            print(f"UV number information of {region} is none.")
            return (None, None)
        _uv_non_num_content_point = _uv_content.find(_uv_num)+len(_uv_num)
        _uv_non_num_content = _uv_content[_uv_non_num_content_point: ]
        return (_uv_num, _uv_non_num_content)
    
    
    def _get_dust_and_ozone_information(self, region, soup):
        _fine_dust = None
        _fine_dust_num = None
        _ultra_fine_dust = None
        _ultra_fine_dust_num = None
        _ozone = None
        _ozone_num = None
        _dust_list = []
        _ozone_text = ""
        for ele in soup.find_all('dd'):
            if "㎍/㎥" in ele.text:
                _dust_list.append(ele.text)
            elif "ppm" in ele.text:
                _ozone_text = ele.text
        try:
            if 'null' not in _dust_list[0].split("㎍/㎥"):
                _fine_dust = _dust_list[0].split("㎍/㎥")[1]
                _fine_dust_num = _dust_list[0].split("㎍/㎥")[0]
            else:
                print(f"Some fine dust information of {region} are missing.")
        except IndexError:
            print(f"All fine dust information of {region} are none.")
           
        try:
            if 'null' not in _dust_list[1].split("㎍/㎥"):
                _ultra_fine_dust = _dust_list[1].split("㎍/㎥")[1]
                _ultra_fine_dust_num = _dust_list[1].split("㎍/㎥")[0]
            else:
                print(f"Some ultra fine dust information of {region} are missing.")
        except IndexError:
            print(f"Ultra fine dust information of {region} are none.")
            
        if _ozone_text is not '':
            _ozone = _ozone_text.split("ppm")[1]
            _ozone_num = _ozone_text.split("ppm")[0]
        else:
            print(f"Ozone information of {region} is none.")
        
        _value_dict = {}
        _value_dict['fine_dust'] = _fine_dust 
        _value_dict['fine_dust_num'] = _fine_dust_num 
        _value_dict['ultra_fine_dust'] = _ultra_fine_dust 
        _value_dict['ultra_fine_dust_num'] = _ultra_fine_dust_num 
        _value_dict['ozone'] = _ozone 
        _value_dict['ozone_num'] = _ozone_num
        return _value_dict
            
            
if __name__ == "__main__":
    weather_info = WeatherInformationCralwer()
    weather_info.main()
    print(weather_info.data_dict)