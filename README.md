1. 找到对应版本的[chromedriver](http://chromedriver.storage.googleapis.com/index.html)
2. 目前selenium版本的会出现一个这样的问题：首先通过百度搜索得到了一个页面结果A,然后设置时间后再次搜索得到页面结果B，想在B中获得对应的搜索数量，但是可能因为此时请求还未响应从而得到了A中的搜索数量。利用了wait和EC方法也没有作用，暂不清楚原因


当前版本使用的是request，使用时需要自己去浏览器中把cookie取出来。

请求头中的`referer`使用了bing的网址，似乎可以躲掉反爬机制。

目前存在的速度限制：
1. `print`打印，之后只将错误情况打印出来
2. `logger`写日志，是否能转换为异步写