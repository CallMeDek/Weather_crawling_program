from collections import defaultdict
import sys


class LoginInformation:
    def __init__(self):
        self._host=None
        self._port=None
        self._user=None
        self._password=None
        self._db_name=None
        self._charset=None
        
        
    @property
    def host(self):
        if self._host is None:
            print("Nothing is aligned to host. Please check.")
            sys.exit(0)
        return self._host
    
       
    @property
    def port(self):
        if self._port is None:
            print("Nothing is aligned to port. Please check.")
            sys.exit(0)
        return self._port
    
 
    @property
    def user(self):
        if self._user is None:
            print("Nothing is aligned to user. Please check.")
            sys.exit(0)
        return self._user
    
             
    @property
    def password(self):
        if self._password is None:
            print("Nothing is aligned to password. Please check.")
            sys.exit(0)
        return self._password
    
         
    @property
    def db_name(self):
        if self._db_name is None:
            print("Nothing is aligned to db_name. Please check.")
            sys.exit(0)
        return self._db_name
    

    @property
    def charset(self):
        if self._charset is None:
            print("Nothing is aligned to charset. Please check.")
            sys.exit(0)
        return self._charset
    
    
    def _set_host(self, host_name):
        if len(host_name) == 0:
            print("Host name is empty. Please check.")
            sys.exit(0)
        self._host=host_name
        
        
    def _set_port(self, port_number):
        if len(port_number) == 0:
            print("Port number is empty. Please check.")
            sys.exit(0)
        self._port=port_number
        
        
    def _set_user(self, user_name):
        if len(user_name) == 0:
            print("User_name is empty. Please check.")
            sys.exit(0)    
        self._user=user_name
        
        
    def _set_password(self, passwrd):
        if len(passwrd) == 0:
            print("Passwrd is empty. Please check.")
            sys.exit(0)       
        self._password=passwrd
        
        
    def _set_db_name(self, database_name):
        if len(database_name) == 0:
            print("Database name is empty. Please check.")
            sys.exit(0)          
        self._db_name=database_name
        
        
    def _set_charset(self, charset_type):
        if len(charset_type) == 0:
            print("charset type is empty so it is set to utf8.") 
            self._charset = 'utf8'
            return
        self._charset=charset_type

        
    def main(self):
        self._read_login_information_file()
    
    
    def _read_login_information_file(self):
        try:
            #_login_file = open('./test_case/login/login_information_charset.txt', 'rt', encoding='utf8')
            _login_file = open('./login_information.txt', 'rt', encoding='utf8')
        except FileNotFoundError as e:
            print("The file containing database login information doesn't exist in the same path. Please check.")
            sys.exit(0)
        _info_list = _login_file.readlines()
        _info_dict = defaultdict(str)
        for info in _info_list:
            key = info.strip().split("=")[0]
            value = info.strip().split("=")[1]
            _info_dict[key] = value
        _key_set = {'host', 'port', 'user', 'passwd', 'db', 'charset'}
        if len(_key_set - set(_info_dict.keys())) > 0:
            print("Some keys are missing. Please check.")
            sys.exit(0)
        self._set_host(_info_dict['host'])   
        self._set_port(_info_dict['port'])
        self._set_user(_info_dict['user'])
        self._set_password(_info_dict['passwd'])
        self._set_db_name(_info_dict['db'])
        self._set_charset(_info_dict['charset']) 
        _login_file.close()
        
  
if __name__ == "__main__":
    login = LoginInformation()
    login.main()
    print(login.host)
    print(port)
    print(user)
    print(password)
    print(db_name)
    print(charset)