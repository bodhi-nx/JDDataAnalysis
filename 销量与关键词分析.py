import jieba
import pymongo
from PIL import Image
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# from scipy.misc import imread
import matplotlib

client = pymongo.MongoClient('localhost', 27017)
db = client['jdspider']
table = db['衬衣']

# 读取数据
data = pd.DataFrame(list(table.find()))
data.head()
# print(data)
# 选择需要显示的字段
title = data[['title']]
sale = data[['comment']]
print(sale)
# 将所有商品标题转换为list
# print(data)

# title = data.raw_title.values.tolist()
comment_after_split = jieba.cut(str(title), cut_all=False)
# 用空格进行拼接
words = ' '.join(comment_after_split)

# 加载停用词
# stopwords = STOPWORDS
# jieba.load_userdict(r'C:\Users\TR\Desktop\毕设\新建文件夹\stopwords.txt')
# 对每个标题进行分词，使用jieba分词


title_s = []
for line in title:
    title_cut = jieba.lcut(line)
    title_s.append(title_cut)

# 导入停用此表

stopwords = [line.strip() for line in open(r'C:\Users\TR\Desktop\毕设\新建文件夹\stopwords.txt', 'r', encoding='utf-8').readlines()]

# 剔除停用词
title_clean = []
for line in title_s:
    line_clean = []
    for word in line:
        if word not in stopwords:
            line_clean.append(word)
    title_clean.append(line_clean)
# 进行去重
title_clean_dist = []
for line in title_clean:
    line_dist = []
    for word in line:
        if word not in line_dist:
            line_dist.append(word)
    title_clean_dist.append(line_dist)

# 将 title_clean_dist 转化为一个list
allwords_clean_dist = []
for line in title_clean_dist:
    for word in line:
        allwords_clean_dist.append(word)
title2 = allwords_clean_dist
# 把列表 allwords_clean_dist 转为数据框
df_allwords_clean_dist = pd.DataFrame({
    'allwords': allwords_clean_dist
})

# 对过滤_去重的词语 进行分类汇总
word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
word_count.columns = ['word', 'count']


plt.figure(figsize=(20,10))

# 读取图片
# pic = imread("背景.png")
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
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()


def dealSales(x):
    x = x.split('人')[0]
    if len(x) == 0:
        return '0'
    if ' 'in x:
        x = x.replace(' ', '')
    if '万' in x:
        if '+' in x:
            x = x.replace('.', '').replace('万', '000')
        else:
            x = x.replace('万', '0000')

    return x.replace('+', '')


data['comment'] = data.comment.apply(lambda x: dealSales(x))
# print(data['comment'])
# 将comment列的数据类型改为int类型


# data['comment'] = data['comment'].map(lambda x: x**1)
data['comment'] = data['comment'].apply(int)

data = data.reset_index(drop=True)

# 不同关键词word对应的sales之和的统计分析
w_s_sum = []
for w in word_count.word:
    i = 0
    s_list = []
    for t in title_clean_dist:
        if w in t:
            s_list.append(data.comment[i])
        i += 1
    w_s_sum.append(sum(s_list)) # list求和


df_w_s_sum = pd.DataFrame({'w_s_sum': w_s_sum})
print(df_w_s_sum)
# 把 word_count 与对应的 df_w_s_sum 合并为一个表:
df_word_sum = pd.concat([word_count, df_w_s_sum],
                        axis=1, ignore_index=True)
df_word_sum.columns = ['word', 'count', 'w_s_sum']  # 添加列名
df_word_sum.sort_values('w_s_sum', inplace=True, ascending=True) # 升序
df_w_s = df_word_sum.tail(30)  # 取最大的30行数据
# print(df_w_s)
font = {'family': 'SimHei'}  # 设置字体
matplotlib.rc('font', **font)

index = np.arange(df_w_s.word.size)
plt.figure(figsize=(100, 200))
plt.barh(index, df_w_s.w_s_sum, color='blue', align='center')
plt.yticks(index, df_w_s.word, fontsize=20)

#添加数据标签
for y, x in zip(index, df_w_s.w_s_sum):
    plt.text(x, y, '%.0f' %x, ha='left', va='center', fontsize=15)
plt.show()




plt.figure(figsize=(60, 40))
plt.hist(data['price'], bins=10, color='blue')
plt.xlabel('价格', fontsize=50)
plt.ylabel('商品数量', fontsize=50)
plt.title('不同价格对应的商品数量分布', fontsize=17)
plt.tick_params(labelsize=30)
plt.xticks(size='small', rotation=20, fontsize=10)
ax.xaxis.set_major_locator(MultipleLocator(6))
plt.show()

flg, ax = plt.subplots()
ax.scatter(data['price'],
          data['comment'], color='blue')
ax.set_xlabel('价格')
ax.set_ylabel('销量')
ax.set_title('商品价格对销量的影响')
plt.xticks(size='small', rotation=20, fontsize=10)
ax.xaxis.set_major_locator(MultipleLocator(6))
plt.show()