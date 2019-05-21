import tushare as ts

indus = ts.get_industry_classified()
indus = indus[indus['c_name']=='金融行业']
indus['code'] = indus['code'].apply(str)
print(indus['code'])
indus.to_csv('C:/Users/Jagga/Documents/finance.csv')