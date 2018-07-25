from selenium import webdriver

browser = webdriver.Chrome('/home/ashwani/chromedriver')
browser.get('localhost:8000')

assert 'Django' in browser.title