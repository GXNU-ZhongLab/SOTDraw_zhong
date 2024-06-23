主要功能：
一、lasot雷达图和曲线图（各挑战属性的曲线图）：python bin/eval.py
先修改启动文件的参数，然后：
（1）修改保存曲线图路径（save_root）：SOTDrawRect-main/toolkit/visualization/draw_success_precision.py
（2）修改保存雷达图pdf路径：SOTDrawRect-main/toolkit/visualization/draw_eao.py draw_eao方法的最后一行

二、画多个跟踪器的跟踪框：python draw_rect.py
修改启动文件的参数。
输出在output里面；可以画单个序列，不指定时默认所有序列

其他：
一、上面的功能应该没问题，目前lasot数据集畅通无阻。如果有其他数据集需求的可以自己尝试。参考源代码：https://github.com/Giveupfree/SOTDrawRect

二、环境：比较简单，一般跟踪器环境就行，缺啥补啥。

三、如果遇到缺失lasot.json的，去找一个放到正确的路径下就可以了：SOTDrawRect-main/toolkit/datasets/lasot.py line：76

四、有些写了绝对路径，应该一眼能看出来是什么路径。例如：/home/data/xcc23/SOTDrawRect-main/toolkit/datasets/lasot.py 里面的line：76、91

