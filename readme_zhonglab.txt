主要功能：
一、lasot雷达图和曲线图（各挑战属性的曲线图）：python bin/eval.py
(1)修改启动文件的参数,主要是数据集路径.
(2)创建保存曲线图和雷达图的文件夹（./toolkit/visualization/draw_success_precision.py里面的save_root）：mkdir ./output/quxiantu
(3)所有的跟踪结果txt文件放在result下的tracker名字命名的文件夹中。

二、画多个跟踪器的跟踪框：python draw_rect.py
修改启动文件的参数。
输出在output里面；可以画单个序列，不指定时默认所有序列

其他：
一、上面的功能应该没问题，目前lasot数据集畅通无阻。如果有其他数据集需求的可以自己尝试。参考源代码：https://github.com/Giveupfree/SOTDrawRect

二、环境：比较简单，一般跟踪器环境就行，缺啥补啥。

三、有些写了绝对路径，应该一眼能看出来是什么路径。例如：./toolkit/datasets/lasot.py 里面的line：91

