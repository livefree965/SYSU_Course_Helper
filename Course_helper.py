import tkinter
import requests
from bs4 import BeautifulSoup
from time import ctime,sleep

msgs = [
        '提交成功',
        '非法操作! 数据库没有对应的教学班号。',
        '当前不在此课程类别的选课时间范围内！',
        '您不在该教学班的修读对象范围内，不允许选此教学班！',
        '您所在的学生群体，在此阶段不允许对该课程类别的课进行选课、退课！',
        '系统中没有您这个学期的报到记录，不允许选课。请联系您所在院系的教务员申请补注册。',
        '您这个学期未完成评教任务，不允许选课。',
        '您不满足该教学班选课的性别要求，不能选此门课程！',
        '不允许跨校区选课！',
        '此课程已选，不能重复选择！',
        '您所选课程 的成绩为“已通过”，因此不允许再选该课，请重新选择！',
        '此类型课程已选学分总数超标',
        '此类型课程已选门数超标',
        '毕业班学生，公选学分已满，最后一个学期不允许选择公选课！',
        '您不是博雅班学生，不能选此门课程！',
        '您最多能选2门博雅班课程！',
        '您不是基础实验班学生，不能选此门课程！',
        '所选课程与已选课程上课时间冲突,请重新选择!',
        '已经超出限选人数，请选择别的课程！',
        '该教学班不参加选课，你不能选此教学班！',
        '选课等待超时',
        '您这个学期未完成缴费，不允许选课。请联系财务处帮助台（84036866 再按 3）',
        '您未满足选择该课程的先修课程条件!',
        '不在此课程类型的选课时间范围内',
        '您的核心通识课学分已满足培养方案的学分要求，无法再选择核心通识课',
        '您的主修必专绩点未达到精英课的选课要求',
        '您已选可互认课程的同组课程',
        '及格重修选课只能选已通过的课程',
        '您不在教学班撤消后抢选的学生名单中',
        '您不是卓越班学生，不能选此门课程！',
        '早前的选课不允许退课！'
        ]
class CourseSystem:
    __DataHandlerObj = ""
    __FoundCourse = ""

    # 初始化创建DataHandler对象
    def __init__(self, username=None, password=None):
        self.__DataHandlerObj = DataHandler(username, password)

    # 对DataHandler对象进行登陆操作
    def Log(self):
        self.__DataHandlerObj.Log()

    # 打印用户信息
    def Printuserinfo(self):
        user_data = self.__DataHandlerObj.Getuserinfo()
        print(user_data[0] + user_data[1] + '\n' + user_data[2] + user_data[3])

    # 打印选课结果
    def PrintCourseRes(self):
        for info in self.__DataHandlerObj.GetCourseResult():
            print(info)

    # 打印可选课程以及选课情况
    def PrintAllCourse(self, choose,removeconflict=0,sort_name="None",isreverse=0):
        all_course_data = self.__DataHandlerObj.GetAllCourse(choose)
        print("已选课程：")
        for data in all_course_data[0]:
            print(data)
        print("提供课程：")
        if sort_name=="None" :
            for data in all_course_data[1]:
                if (not removeconflict) or data[9]!='forbid_elect':
                    print(data)
        else:
            for data in sorted(all_course_data[1],key=lambda course:course[sort_name],reverse=1):
                if (not removeconflict) or data[9]!='forbid_elect':
                    print(data)

    # 选课
    def ChooseCourseFeedBack(self, pos, oper):
        status = self.__DataHandlerObj.ChooseCourse(self.__FoundCourse[pos], oper)
        return int(status[15])

    # 打印目标课程
    def PrintFoundCourse(self, keyword):
        print("搜索结果：")
        self.__FoundCourse = self.__DataHandlerObj.FindCourse(keyword)
        for course in self.__FoundCourse:
            print(course)
        print("查找结束,总共找到" + str(len(self.__FoundCourse)) + "个结果")


class DataHandler:
    __logpage = ""
    __logData = ""
    __main_session = ""
    __main_page = ""
    __main_page_soup = ""
    __sid = ""
    __xkjdsizd = ""

    # 对象初始化
    def __init__(self, username, password):
        self.__main_session = requests.session()
        self.__log_page = self.__main_session.get(url='http://uems.sysu.edu.cn/elect/casLogin')
        log_page_soup = BeautifulSoup(self.__log_page.content, 'html.parser')
        self.__logData = {
            "username": username,
            "password": password,
            "lt": log_page_soup.find_all('input')[2]['value'],
            "execution": log_page_soup.find_all('input')[3]['value'],
            "_eventId": "submit",
            "submit": "登陆"
        }

    # 登陆
    def Log(self):
        self.__main_page = self.__main_session.post(url=self.__log_page.url, data=self.__logData)
        self.__main_page_soup = BeautifulSoup(self.__main_page.text, 'html.parser')
        if  'Connection' in self.__main_page.headers :
            raise Exception("登陆失败,请检查用户名和密码！")
        else:
            allxkj = self.__main_page_soup.findAll('a', href=True)
            self.__sid = self.__main_page.url.split('=')[1]
            self.__xkjdsizd = [allxkj[0]['href'][17:30], allxkj[1]['href'][17:30], allxkj[2]['href'][17:30],
                               allxkj[3]['href'][17:30]]
        return True
    # 返回一个列表包含用户信息
    def Getuserinfo(self):
        result_page = self.__main_session.get(
            'http://uems.sysu.edu.cn/elect/s/' + self.__main_page_soup.findAll('a', href=True)[4]['href'])
        result_soup = BeautifulSoup(result_page.text, 'html.parser')
        user_data = result_soup.find('tr', class_=['odd', 'even'])
        return [user_data.findAll('td')[0].string, user_data.findAll('td')[1].string, user_data.findAll('td')[2].string,
                user_data.findAll('td')[3].string]

    # 获取选课结果
    def GetCourseResult(self):
        print("选课结果为：")
        result_page = self.__main_session.get(
            'http://uems.sysu.edu.cn/elect/s/' + self.__main_page_soup.findAll('a', href=True)[4]['href'])
        courseresultdata = []
        for info in BeautifulSoup(result_page.text, 'html.parser').find('div', id='content').findAll('tr',
                                                                                                     class_=['odd',
                                                                                                             'even']):
            info_text = info.findAll('td')
            courseresultdata.append([info_text[0].string, info_text[1].string, info_text[2].string, info_text[3].string,
                                     info_text[4].string, info_text[5].string, info_text[6].string, info_text[7].string,
                                     info_text[8].string.strip(), info_text[9].string])
        return courseresultdata

    # 获取某一类型的所有课程
    def GetAllCourse(self, courseclass):
        all_course_page = self.__main_session.get(
            'http://uems.sysu.edu.cn/elect/s/' + self.__main_page_soup.findAll('a', href=True)[courseclass]['href'])
        elected = []
        unelect = []
        res = []
        for info in BeautifulSoup(all_course_page.text, 'html.parser').findAll('tbody')[0].findAll('tr'):
            info_text = info.findAll('td')
            if info_text[0].text.find('退选') >= 1:
                elected.append(
                    [info_text[1].string, info_text[2].string.strip(), info_text[3].string, info_text[4].string,
                     info_text[5].string, info_text[6].string, info_text[7].string, info_text[8].string.strip(),
                     info_text[9].string, info.find('a')['jxbh'], courseclass])
            else:
                elected.append(
                    [info_text[1].string, info_text[2].string.strip(), info_text[3].string, info_text[4].string,
                     info_text[5].string, info_text[6].string, info_text[7].string, info_text[8].string.strip(),
                     info_text[9].string, "forbid_unelect", courseclass])
        for info in BeautifulSoup(all_course_page.text, 'html.parser').findAll('tbody')[1].findAll('tr'):
            info_text = info.findAll('td')
            if  info_text[0].text.find('选课') >= 1:
                unelect.append(
                    [info_text[1].string, info_text[2].string.strip(), info_text[3].string, info_text[4].string,
                     info_text[5].string, info_text[6].string, info_text[7].string, info_text[8].string.strip(),
                     info_text[9].string, info.find('a')['jxbh'], courseclass])
            else:
                unelect.append(
                    [info_text[1].string, info_text[2].string.strip(), info_text[3].string, info_text[4].string,
                     info_text[5].string, info_text[6].string, info_text[7].string, info_text[8].string.strip(),
                     info_text[9].string, "forbid_elect", courseclass])
        res.append(elected)
        res.append(unelect)
        return res

    # 选课
    def ChooseCourse(self, coursedata, oper):
        choose_data = {
            "jxbh": coursedata[9],
            "sid": self.__sid
        }
        ret = ""
        r = self.__main_session
        if oper == 'elect':
            choose_data["xkjdsizd"] = self.__xkjdsizd[coursedata[10]]
            ret = self.__main_session.post(url='http://uems.sysu.edu.cn/elect/s/elect', data=choose_data)
        else:
            choose_data["xkjdszid"] = self.__xkjdsizd[coursedata[10]]
            ret = self.__main_session.post(url='http://uems.sysu.edu.cn/elect/s/unelect', data=choose_data)
        status = BeautifulSoup(ret.text, 'html.parser')
        return status.text

    # 寻找符合关键字的课程并以列表形式返回
    def FindCourse(self, keyword):
        objlist = []
        for courseclass in range(4):
            for courseset in self.GetAllCourse(courseclass):
                for course in courseset:
                    for coursecontent in course[0:4]:
                        if str(coursecontent).find(keyword) > -1:
                            objlist.append(course)
        return objlist

def log():
    global COURSE_HELPER
    print(">>>双鸭山选课系统v1.0")
    print(">>>输入数字选取相应功能")
    print(">>>1.登陆 2.退出")
    user_input=int(input())
    if user_input==2:
        exit()
    print(">>>请输入账号")
    username=input()
    print(">>>请输入密码")
    password=input()
    print(">>>正在登陆，请稍候...")
    COURSE_HELPER=CourseSystem(username,password)
    COURSE_HELPER.Log()
    print("登陆成功\n用户信息如下:")
    COURSE_HELPER.Printuserinfo()
def execute():
    global COURSE_HELPER
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>输入数字获取相应功能")
    print(">>>1.选课")
    print(">>>2.查看选课结果")
    print(">>>3.查看某课程范围课程情况")
    print(">>>4.查找相关课程")
    print(">>>5.退出")
    user_input=int(input())
    if user_input==5:
        exit()
    elif user_input==1:
        COURSE_HELPER.PrintFoundCourse(input(">>>请输入课程关键字（支持模糊搜索）\n"))
        index_choose=int(input(">>>请输入需要执行的操作 1.选课 2.退选\n"))
        pos_choose=int(input(">>>请输入目标课程序号（列表第一个则输入1）\n"))-1
        status=-1
        global msgs
        if index_choose==1:
            while status!=0:
                status=COURSE_HELPER.ChooseCourseFeedBack(pos_choose,'elect')
                print(msgs[status])
                sleep(1)
        else:
            while status!=0:
                status = COURSE_HELPER.ChooseCourseFeedBack(pos_choose, 'unelect')
                print(msgs[status])
                sleep(1)
        print(">>>操作完成")
    elif user_input==2:
        COURSE_HELPER.PrintCourseRes()
    elif user_input==3:
        print(">>>输入数字获取对应功能，输入help获取对应帮助")
        class_input = input()
        if class_input=="help":
            print(">>>第一个数字：1.公必 2.专必 3.专选 4.公选")
            print(">>>第二个数字：0.不排除冲突 1.排除冲突")
            print(">>>第三个数字：0.按空位排序 1.按选中率排列")
            print(">>>第四个数字：0.按升序排列 1.按降序排列")
            print(">>>默认情况下不排除冲突不进行排序")
            print(">>>例：输入1 1 2 3代表输出公必中不冲突的课程，并且按照空位升位排序")
        else:
            input_set=class_input.split()
            if(len(input_set)==4):
                COURSE_HELPER.PrintAllCourse(int(input_set[0])-1,int(input_set[1]),int(input_set[2])+7,int(input_set[3]))
            elif(len(input_set)==2):
                COURSE_HELPER.PrintAllCourse(int(input_set[0]) - 1, int(input_set[1]))
            else:
                COURSE_HELPER.PrintAllCourse(int(input_set[0]) - 1)
    else:
        COURSE_HELPER.PrintFoundCourse(input(">>>请输入课程关键字（支持模糊搜索）\n"))

if __name__ == "__main__":
    COURSE_HELPER=CourseSystem()
    log()
    while True:
        execute()
