# scrawl_demo
## scral_comic_1.py
爬取的一个网站的漫画
requests demo, 最最重要点是在headers中加入referer，爬虫才不会被拦截掉，另外添加了本地保存

## scral_comic_2.py
这个单独用requests行不通，最终解决方案是
用phan打开网页，找到节点
先BS爬取节点，找到图片地址然后
requests下载图片

通过模拟浏览器打开来爬取，虽然慢了一些但是够用就好了

## lagou.py
爬取拉勾职位的一些平均工资，第一版写的很渣，需要手动粘贴岗位的URL，还没有连接数据库
