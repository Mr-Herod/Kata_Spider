"""这个程序只针对codewars网站有效"""

环境配置：

1、安装 Google Chrome 浏览器
2、安装 selenium 包（ cmd 输入pip install -U selenium 通过pip安装selenium）
3、安装 chromedriver.exe 
      教程：https://jingyan.baidu.com/article/f7ff0bfcdd89ed2e27bb1379.html
4、安装 BeautifulSoup 包（ cmd 输入pip install beautilfulsoup4 通过pip安装BeautifulSoup）
      教程：https://jingyan.baidu.com/article/e75aca853569b6142edac6d4.html
5、配置好一切之后就可以开始运行了

注意事项：
1、程序运行需要给出 URL链接 和 文件保存目录 两个参数，会有输入提示
     
     地址需要一个目录的绝对路径  例如：C:\Users\xxxxxx\Desktop\test\
     
     注意这里需要的是一个  目录  的路径，而且需要先进行创建
     
     URL链接需要的是solution页面的链接
     例如 ：https://www.codewars.com/users/xxxxxx/completed_solutions

2、第一次爬取需要获取cookie值  也就是需要登陆

     所以第一次运行的时候会有一个页面弹出来，然后需要在20秒内完成登陆。

     以后就不用了

3、接下来  就可以一边吃瓜一边看着它整理代码了  ^_^ .