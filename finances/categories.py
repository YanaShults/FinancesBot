cat = ['food', 'clothes', 'entertainment', 'dancing', 'sport',
       'transport', 'house', 'cafe', 'cosmetics',
       'subscriptions', 'utilities', 'medication', 'communicat_internet',
       'other']
str_cat = ' ,'.join(cat)
count_cat = len(cat)

list_cat_db = [i+' INTEGER' for i in cat]
# print(list_cat_db)
str_cat_db = ' ,'.join(list_cat_db)
# print(str_cat_db)