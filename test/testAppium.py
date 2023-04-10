from appium.webdriver import Remote  #引入打开软件的包

#app的启动参数
desired_cap={
    "platformName":"Android",   #手机系统
    "platformVersion": "9",  #手机系统版本
    "deviceName":'HUAWEI',  #手机的名字，不会进行校验，但是没有会报错
    "automationName":"UiAutomator2",#自动化测试框架 （1.4以上的appium不用写）
    "appPackage":"com.taobao.taobao",#app包名
    "appActivity":"com.taobao.tao.welcome.Welcome",#app的启动页面
}

driver = Remote(command_executor='http://127.0.0.1:4723/wd/hub',desired_capabilities=desired_cap)