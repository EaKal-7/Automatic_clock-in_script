#coding:utf-8
import time
import email
import smtplib
import traceback
from email.mime.text import MIMEText
from selenium import webdriver


#这里对浏览器进行设置，防止在后面find函数报错
WIDTH = 600  # 宽度
HEIGHT = 840  # 高度
PIXEL_RATIO = 3.0  # 分辨率

mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

#这里是对账号进行设置
uid="***************"   #E浙理账号
pwd="***********"       #E浙理密码
def sendmail(subject, content):
    email_user = '************'  # 发送者账号
    email_pwd = '*********'       # 发送者授权码
    maillist ='*********'    # 接收者账号，本来想写成[]list的，但是报错，还没解决！
    me = email_user

    msg = MIMEText(content, 'html', 'utf-8')    # 邮件内容，三个参数：第一个为文本内容，第二个 html 设置文本格式，第三个 utf-8 设置编码
    msg['Subject'] = subject    # 邮件主题
    msg['From'] = me    # 发送者账号
    msg['To'] = maillist    # 接收者账号列表（列表没实现）

    smtp = smtplib.SMTP("smtp.qq.com",587) # 如上变量定义的，是qq邮箱,不要用25端口，会被阿里云禁用的
    smtp.login(email_user, email_pwd)   # 发送者的邮箱账号，密码
    smtp.sendmail(me, maillist, msg.as_string())    # 参数分别是发送者，接收者，第三个不知道
    smtp.quit() # 发送完毕后退出smtp
    print ('email send success.')




try:
    # 模拟浏览器进行访问
    browser = webdriver.Chrome(chrome_options=options)
    browser.get("http://stu.zstu.edu.cn/webroot/decision/login?origin=a5402a14-e210-4d84-a85c-51a48879c1f5")
    browser.find_element_by_xpath("//*[@placeholder='用户名']").send_keys(uid)
    browser.find_element_by_xpath("//*[@placeholder='密码']").send_keys(pwd)
    browser.find_element_by_xpath("//*[@id='wrapper']/div[1]/div/div[2]/div/div/div/div[6]/div").click()
    #以上为E浙理的登陆，这个Xpath搞了我好久nnd
    time.sleep(15)
    #这里sleep5都会卡，服务器是真的垃圾
    browser.find_element_by_xpath("//*[@id='wrapper']/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[5]/div/div/div[1]/div/div[1]/div/div/div[1]/div/div[4]").click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[@id='wrapper']/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[5]/div/div/div[1]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div[3]").click()
    time.sleep(10)
    #browser.switch_to.frame(1)
    elementi= browser.find_element_by_xpath("//*[@id='wrapper']/div[1]/div[1]/div/div[1]/div[1]/div[1]/iframe[2]")
    #再将定位对象传给switch_to_frame()方法
    browser.switch_to_frame(elementi) 
    #以上为E浙理的健康申报的进入，这里没有返回E浙理崩溃的情况
    browser.find_element_by_xpath("//*[@id='D17-0-0']/div/span[1]/div/span").click()
    #第一个37度
    browser.find_element_by_xpath("//*[@id='D18-0-0']/div/span[1]/div/span").click()
    #第二个37度
    browser.find_element_by_xpath("//*[@id='F20-0-0']/div/span[1]/div/span").click()
    #绿码
    browser.find_element_by_xpath("//*[@id='F21-0-0']/div/span[2]/div/span").click()
    #返乡
    browser.find_element_by_xpath("//*[@id='F22-0-0']/div/span[2]/div/span").click()
    #家庭成员
    browser.find_element_by_xpath("//*[@id='F23-0-0']/div/span[2]/div/span").click()
    #
    browser.find_element_by_xpath("//*[@id='F25-0-0']/div/span[2]/div/span").click()
    #
    #常规间隔，因为懒加载所以会卡顿，等待加载
    browser.find_element_by_xpath("//*[@id='F27-0-0']/div/span[1]/div/span").click()
    #
    browser.find_element_by_xpath("//*[@id='F29-0-0']/div/span[2]/div/span").click()
    #
    browser.find_element_by_xpath("//*[@id='F32-0-0']/div/span[2]/div/span").click()
    #
    browser.find_element_by_xpath("//*[@id='F35-0-0']/div/span[2]/div/span").click()
    #
    time.sleep(3)

    browser.find_element_by_xpath("//*[@id='fr-btn-']/div/em/button").click()
    time.sleep(10)
    #这里停留等待最后获取final_text，用作最后服务器或者邮箱返回
    final_text = browser.find_element_by_xpath("//*[@class='fh tac bw f16-0 pl2 b0']").text
    print(final_text)
    browser.quit()
    sendmail(final_text,final_text)
except:
    print('签到失败')
    sendmail('签到失败，傻逼出BUG了，快修','签到失败，傻逼出BUG了，快修\n'+traceback.format_exc())
