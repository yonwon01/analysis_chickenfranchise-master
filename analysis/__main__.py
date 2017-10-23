import pandas as pd
import matplotlib.pyplot as plt

bbq_table = pd.DataFrame.from_csv('../__result__/crawling/bbq_table.csv', encoding='utf-8', index_col=0, header=0)
bbq = bbq_table.apply(lambda r: r['sido'] + ' ' + r['gungu'], axis='columns').value_counts()

kyochon_table = pd.DataFrame.from_csv('../__result__/crawling/kyochon_table.csv', encoding='utf-8', index_col=0, header=0)
kyochon = kyochon_table.apply(lambda r: r['sido'] + ' ' + r['gungu'], axis='columns').value_counts()

nene_table = pd.DataFrame.from_csv('../__result__/crawling/nene_table.csv', encoding='utf-8', index_col=0, header=0)
nene = nene_table.apply(lambda r: r['sido'] + ' ' + r['gungu'], axis='columns').value_counts()

pelicana_table = pd.DataFrame.from_csv('../__result__/crawling/pelicana_table.csv', encoding='utf-8', index_col=0, header=0)
pelicana = pelicana_table.apply(lambda r: r['sido'] + ' ' + r['gungu'], axis='columns').value_counts()

chicken_table = pd.DataFrame({'bbq': bbq, 'kyochon': kyochon, 'nene': nene, 'pelicana': pelicana}).fillna(0)

plt.figure()
chicken_table.sum(axis=0).iloc[:4].plot(kind='bar')

plt.show()

