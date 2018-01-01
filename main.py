from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("http://www.acorn.utoronto.ca/")
login = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/p[2]/a").click()
username = driver.find_element_by_xpath("//*[@id=\"inputID\"]")
username.clear()
username.send_keys("chenmi84")
pwd = driver.find_element_by_xpath("//*[@id=\"inputPassword\"]")
pwd.clear()
pwd.send_keys("Harry6966xx511")
submit = driver.find_element_by_xpath("//*[@id=\"query\"]/button")
submit.click()
submit.click()

academic = driver.get("https://acorn.utoronto.ca/sws/transcript/academic/main.do?main.dispatch")
content = driver.page_source

soup = BeautifulSoup(content)
print(soup)
#




