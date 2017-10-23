import pandas as pd

table = pd.DataFrame.from_csv(
    '../__result__/crawling/bbq_table.csv',
    encoding='utf-8',
    index_col=0,
    header=0)
# 중복 확인
print(table.count())
table = table.drop_duplicates(subset='name', keep='first')
print(table.count())

# 문제는 인덱스가 빠짐 재인덱싱 필요
t = pd.DataFrame({'name': ['a', 'b', 'c', 'b', 'd']})
print(t)
t = t.\
    drop_duplicates(subset='name', keep='first').\
    reset_index(drop=True)
print(t)