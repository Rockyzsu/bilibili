# B站视频下载

* 自动批量下载B站一个系列的视频
* 下载某个UP主的所有视频



* 使用：

  下载you-get库，git clone https://github.com/soimort/you-get.git 复制其本地路径，比如/root/you-get/you-get

  初次运行，删除history.db 文件， 修改配置文件config.py

  ```
  START=1 # 下载系列视频的 第一个
  END=1 # 下载系列视频的最后一个 ， 比如一个系列教程有30个视频， start=5 ,end = 20 下载从第5个到第20个
  ID='BV1oK411L7au' # 视频的ID
  YOU_GET_PATH='/home/xda/othergit/you-get/you-get' # 你的you-get路径
  MINS=1 # 每次循环等待1分钟
  user_id = '518973111' # UP主的ID
  total_page = 3 # up主的视频的页数
  ```

  

  执行 python downloader.py ，进行下载循环

  python people.py ，把某个up主的视频链接加入到待下载队列

  python add_data.py --id=BV1oK411L7au --start=4 --end=8 下载视频id为BV1oK411L7au的系列教程，从第4开始，到第8个结束，如果只有一个的话，start和end设为1即可。

  可以不断地往队列里面添加下载链接。

