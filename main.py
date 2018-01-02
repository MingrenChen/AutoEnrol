from selenium import webdriver
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

global count
# driver = webdriver.Chrome()
def renew_grade():
    global count
    count += 1
    print("operation number {}, now is".format(count), datetime.now())
    driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNITWITHJS)
    driver.get("http://www.acorn.utoronto.ca/")
    driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/p[2]/a").click()
    print("able to enter username/pwd")
    username = driver.find_element_by_xpath("//*[@id=\"inputID\"]")
    username.clear()
    username.send_keys("chenmi84")
    pwd = driver.find_element_by_xpath("//*[@id=\"inputPassword\"]")
    pwd.clear()
    pwd.send_keys("Harry6966xx511")
    submit = driver.find_element_by_xpath("//*[@id=\"query\"]/button")
    submit.click()
    print("login")
    try:
        submit.click()
    except:
        pass

    driver.get("https://acorn.utoronto.ca/sws/transcript/academic/main.do?main.dispatch")
    content = driver.page_source

    soup = BeautifulSoup(content,"lxml")
    lst1 = soup.find(class_ = "academic-history-recent").find_all(class_ = "courses")

    def deletet(string):
        new_str = ''
        for i in string:
            if not i == '\n' and '\t':
                new_str += i
        if new_str != '':
            return int(new_str)
        return None


    mark = {}
    for course in lst1:
        mark[course.find('td').string] = deletet(course.find(class_ = 'course-mark').string)
    try:
        with open("grade.json", 'r') as data:
            last_ = json.load(data)
    except:
        print("here")
        json.dump(mark, open("grade.json", 'w'))
        with open("grade.json", 'r') as data:
            last_ = json.load(data)


    msg = ""
    if last_ != mark:
        print("there's something different")
        for i in mark:
            if mark[i] != last_[i]:
                if last_[i] is None:
                    msg += "{}'s mark is out, you got {}\n".format(i, mark[i])
                else:
                    msg += "{}'s mark is change, you get {} now\n".format(i, mark[i])
            else:
                print(i, "is the same")
        json.dump(mark, open("grade.json", 'w'))
    else:
        print("everything keeps the same")


    msg = MIMEText(msg)
    me = 'autoRemainder@aspada.life'
    you = 'chenmr9769@gmail.com'
    msg['Subject'] = 'Your grade has been changed.'
    msg['From'] = me
    msg['To'] = you

    s = smtplib.SMTP('localhost')
    s.sendmail(me, [you], msg.as_string())
    s.quit()



scheduler = BlockingScheduler()
scheduler.add_job(renew_grade(), 'interval', hours=1)
scheduler.start()