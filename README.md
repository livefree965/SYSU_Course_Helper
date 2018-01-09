
# SYSU Course Helper

![][1] ![][2] ![][3] ![][4] ![][5]

A tool aiming to help the student in Sun Yat-Sen University in Chinese mainland elect course more efficiently,is written by Python.It offers functions including checking courses,electing and unelecting courses,seeking courses by keyword and so on.Besides,you can easily get the data by import the py,and develop what you want based on it.The project provides the source code and the executable file packed by pyinstaller.You can just download the executable file for use.

## 中文指引

- 尚未更新打包二进制文件，需要的同学请自行根据要求配置环境
- 相关功能尚未完善，有问题请[submit issue][9]
- 将会在寒假期间进行大规模更新，欢迎Star
- 稳定的功能是监控选课，大家可以挂着捡漏...(Tips:间隔请合理设置不要太频繁)

## Update log

- v 1.2(2018.1.9)
  - Amendments to the elective system update, adding CAPTCHA mechanism
- v 1.1(2017.7.20)
  - Fix the bug: An error is reported when there is no class in a category
- v 1.0(2017.7.14)
  - The first version release, to achieve the basic functions

## Requirement

You can use it without any reqirement by executable file,but if you'd like to execute the source code,you need these:

- Python environment(3.6.0 and above)
- Requests(2.18.1 and above)
- Beautifulsoup4(4.6.0 and above)

## Quick Start

- Download button is above the Project File,you can click to download it
- You can just execute the program and follow the notifiction
- The program hasn't have English version,if you need that,just contact me on github

## Installation

- Python environment:[Click Here][6]
- Requests:For windows you can change directory to Python installation directory and find the Script file and enter `./pip install requests` in Windows Powershell(Administration Request).For linux you can just `pip install requests`,you can learn more from [Click Here][7]
- Beautifulsoup4:As Requests you can also enter `pip install beautifulsoup4`,you can learn more from [Click Here][8]

## For developer

You can `import Course_helper` or `From Course_helper import DataHandler` in your program.One of the important things is a course data is store by a list.DataHandler is a class and provide these:

- Initialize a new Object,requires username and password as parameter

    ```python
        obj=DataHandler(self,username,password)
    ```

- Log the system,will return True,if log fails it will raise an exception

    ```python
        obj.log(self)
    ```

- Get user's infomation,will return a list=[name,namevalue,ID,IDvalue]

    ```python
        ret=obj.Getuserinfo(self)
        ret=['name','sunyatsen','id','1234']
    ```

- Get user's elected course,return a list include many courses data:

    ```python
        res=obj.GetCourseResult(self)
        res=[[course1,teacher1],[course2,teacher2]]#Some element are ignore
    ```

- Get one of classifications class,require the courseclass code parameter,return a list include two element,the first one is elected coursesdata list,the second one is unelect coursedata list:

    ```python
        res=obj.GetAllCourse(self, courseclass)
        res=[[[course1,teacher1],[course2,teacher2]],[[course3,teacher3],[course4,teacher4]]]
        #Some element are ignore
    ```

- Get the related course,reqiure the keyword as parameter,return a list of courses data
    ```python
        res=objFindCourse(self, keyword)
        res=[[course1,teacher1],[course2,teacher2]]#Some element are ignore
    ```

- Send post to system to elect/unelect course,requires a course data(a list) and the operation(a string as 'elect' or 'unelect') as parameter,return the result code as an integer

    ```python
        objChooseCourse(self, coursedata, operation)
    ```

- You can `From Course_helper import msgs` to check the result code,which is a list,and result code means sucess when it's 0

- The length of a course data is 11(user's elected course data is 10),and the tenth element contains the data which will post to the system.And the others you can print them to check what they means.

## Todo

- Code refactoring
- Exception handling mechanism
- Graphical interface

## Discussing

- [submit issue][9]
- Giving suggestion is welcomed,Thanks for your reading,we are making better

## BLOG

- [My BLOG][10]


[1]: https://img.shields.io/badge/build-passing-brightgreen.svg
[2]: https://img.shields.io/badge/python-3.6.0-blue.svg
[3]: https://img.shields.io/badge/requests-2.18.1-green.svg
[4]: https://img.shields.io/badge/Beautifulsoup-4.6.0-orange.svg
[5]: https://img.shields.io/badge/release-1.0-red.svg
[6]: https://www.python.org/downloads/
[7]: http://www.python-requests.org/en/master/
[8]: https://www.crummy.com/software/BeautifulSoup/
[9]: https://github.com/xiejiangzhao/SYSU_course_helper/issues/new
[10]: http://www.xiejiangzhao.top/