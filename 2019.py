from selenium import webdriver
import time
import requests as re
import json
import os
from prettytable import PrettyTable

d = webdriver.Chrome()
selectedCateMap = {"本专业": 1, "校级公选": 4, "跨专业": 2, "专必": 11, "专选": 21, "院内公选": 30, "公必(体育)": 10, "公必(大英)": 10}
selectedTypeMap = {"本专业": 1, "校级公选": 4, "跨专业": 2, "专必": 11, "专选": 1, "院内公选": 1, "公必(体育)": 3, "公必(大英)": 5}
header = {'Host': 'uems.sysu.edu.cn',
          'Connection': 'keep-alive',
          'Origin': 'https://uems.sysu.edu.cn',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
          'Content-Type': 'application/json;charset=UTF-8',
          'Accept': 'application/json, text/plain, */*',
          'X-Requested-With': 'XMLHttpRequest',
          'moduleId': 'null',
          'menuId': 'null',
          'Referer': 'https://uems.sysu.edu.cn/jwxt/mk/courseSelection/',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9'
          }


class Course_Help:
    def __init__(self):
        self.config = None
        self.brower = None
        self.session = re.Session()

    def load_config(self, filename="config.json"):
        if os.path.exists(filename):
            with open(filename) as f:
                self.config = json.load(f)
                if "cookies" in self.config and self.config["cookies"] != None:
                    self.config["cookies"] = eval(self.config["cookies"])
        else:
            self.config = self.init_config(filename)

    def init_config(self, filename="config.json"):
        config = {}
        config['username'] = None
        config['password'] = None
        config['cookies'] = None
        config["consider_add"] = False
        with open("config.json", 'w') as f:
            json.dump(config, f)
        return config

    def save_config(self, filename="config.json"):
        self.config["cookies"] = str(self.config["cookies"])
        with open(filename, 'w') as f:
            json.dump(self.config, f)

    def login(self):
        tmp = json.loads(self.session.post(
            "https://uems.sysu.edu.cn/jwxt/choose-course-front-server/classCourseInfo/course/list?_t=1547795769",
            cookies=self.config['cookies'], headers=header).text)
        if json.loads(self.session.post(
                "https://uems.sysu.edu.cn/jwxt/choose-course-front-server/classCourseInfo/course/list?_t=1547795769",
                cookies=self.config['cookies'], headers=header).text)["code"] != 53000007:
            return
        # if self.config["cookies"] != None:
        #     return
        self.brower = webdriver.Chrome()
        self.brower.get(
            "https://cas.sysu.edu.cn/cas/login?service=https%3A%2F%2Fuems.sysu.edu.cn%2Fjwxt%2Fapi%2Fsso%2Fcas%2Flogin%3Fpattern%3Dstudent-login")
        try:
            username = self.brower.find_element_by_id("username")
            username.send_keys(self.config["username"])
            password = self.brower.find_element_by_id("password")
            password.send_keys(self.config["password"])
        except:
            pass
        while (self.brower.current_url != "https://uems.sysu.edu.cn/jwxt/#!/student/index"):
            time.sleep(2)
        self.brower.get("https://uems.sysu.edu.cn/jwxt/mk/courseSelection/")
        self.config['cookies'] = {}
        for i in self.brower.get_cookies():
            self.config['cookies'][i['name']] = i['value']
        self.brower.close()

    def get_course(self):
        datas = {"pageNo": 1, "pageSize": 10,
                 "param": {"semesterYear": "2018-2", "selectedType": "1", "selectedCate": "21",
                           "hiddenConflictStatus": "0",
                           "hiddenSelectedStatus": "0", "collectionStatus": "0"}}
        res = self.session.post(
            "https://uems.sysu.edu.cn/jwxt/choose-course-front-server/classCourseInfo/course/list?_t=1547795769",
            cookies=self.config['cookies'], headers=header, data=json.dumps(datas))
        res.encoding = 'utf8'
        course_data = json.loads(res.text)['data']['rows']
        self.print_course(course_data)
        pass

    def print_course(self, course_data):
        form = PrettyTable(["课程号", "课程名", "学分", "考察形式", "已选人数", "剩余空位"])
        for item in course_data:
            if (self.config['consider_add']):
                form.add_row(
                    [item['courseNum'], item['courseName'], item['credit'], item['examFormName'],
                     item['courseSelectedNum'],
                     item['baseReceiveNum'] + item['addReceiveNum'] - int(item['courseSelectedNum'])])
            else:
                form.add_row(
                    [item['courseNum'], item['courseName'], item['credit'], item['examFormName'],
                     item['courseSelectedNum'],
                     item['baseReceiveNum'] - int(item['courseSelectedNum'])])
        print(form)


if __name__ == "__main__":
    course_help = Course_Help()
    course_help.load_config()
    course_help.login()
    course_help.get_course()
    course_help.save_config()
