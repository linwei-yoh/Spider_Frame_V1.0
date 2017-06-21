# Spider_Frame_V1.0

这是一个简易的线程池爬取+进程池解析+redis+mongodb的爬虫框架。

只需要复写overwrite文件下的具体实现就可以完成目标爬虫
Ini文件中可以设置多种参数。例如线程池与进程池的大小，爬取频率，周期等。

该框架参考了笑虎大腿的Pspider。Pspider结构更为简洁，只是没有提供多进程实现。
https://github.com/xianhu/PSpider
