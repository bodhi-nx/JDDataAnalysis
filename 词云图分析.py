from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import numpy as np
import jieba
import matplotlib.pyplot as plt
import pymongo
import pandas as pd
import wordcloud


# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
db = client['jdspider']
table = db['衬衣']

# 读取数据
data = pd.DataFrame(list(table.find()))

# 选择需要显示的字段
data = data[['comments']]
comment_after_split = jieba.cut(str(data), cut_all=False)
# 用空格进行拼接
words = ' '.join(comment_after_split)

# 加载停用词
# stopwords = STOPWORDS
jieba.load_userdict(r'C:\Users\TR\Desktop\毕设\新建文件夹\stopwords.txt')
# 设置屏蔽词
stopwords = STOPWORDS.copy()
stopwords.add('不错')
stopwords.add('下次')
stopwords.add('购物')
stopwords.add('这次')
stopwords.add('可以')
stopwords.add('非常')
stopwords.add('没有')
stopwords.add('有点')
stopwords.add('我用')
stopwords.add('洗衣粉')
stopwords.add('买回来')
stopwords.add('但是')
stopwords.add('那个')
stopwords.add('所以')
stopwords.add('真的')
stopwords.add('怎么')
stopwords.add('保障')
stopwords.add('建议')
stopwords.add('衣服')
stopwords.add('感觉')
stopwords.add('穿着')
stopwords.add('保障')
stopwords.add('收到')
stopwords.add('还会')
stopwords.add('肯定')
stopwords.add('大小')
stopwords.add('打底')
stopwords.add('裤子')
stopwords.add('购买')
stopwords.add('不会')
stopwords.add('出门')
stopwords.add('不但')
stopwords.add('昨天')
stopwords.add('书写')
stopwords.add('喜欢')
stopwords.add('去年')
stopwords.add('第一次')
stopwords.add('这个')
stopwords.add('出门')
stopwords.add('超级')
stopwords.add('大家')
stopwords.add('看看')
stopwords.add('图片')
stopwords.add('爆表')
stopwords.add('手提包')
stopwords.add('一个')
stopwords.add('一些')
stopwords.add('以前')
stopwords.add('商品')
stopwords.add('图片吧')
stopwords.add('特别')
stopwords.add('不错')
stopwords.add('比较')
stopwords.add('朋友')
stopwords.add('钱包')


image = Image.open('背景.png')
# 作为背景形状的图
graph = np.array(image)

wc = WordCloud(width=1000,
                height=600,
                background_color='#f9f9f9',
                font_path='STKAITI.TTF',
                stopwords=stopwords,
                scale=5,
                mask= graph,
                max_font_size=200)
# 将分词的数据传入词云
wc.generate_from_text(words)

plt.imshow(wc)
plt.axis('off')  # 不显示坐标轴
photo_path = r'C:\Users\TR\Desktop\新建文件夹 (2)' + '\\' + '.png'
plt.savefig(photo_path)  # 将词云图存储到本地

print('词云图制作完成！')
wc.to_file(r"wordcloud.png") # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
# 4.显示图片
# 指定所绘图名称
plt.figure("jay")
# 以图片的形式显示词云
plt.imshow(wc)
# 关闭图像坐标系
plt.axis("off")
plt.show()

# 打印输出
#print(data)



