import csv
import pandas as pd


#with open('posts_info.txt', 'r') as in_file:
#    stripped = (line.strip() for line in in_file)
#    lines = (line.split("\n") for line in stripped if line)
#    with open('deals_log.csv', 'w') as out_file:
#        writer = csv.writer(out_file)
#        writer.writerow(('Date', 'City', 'Deal Type', 'Address', 'Market', 'Asset Type', 'Buyer Name', 'Seller Name',
#                         'Broker(s)', 'Price', 'Notes', 'Link'))
#        writer.writerows(lines)

new_temp = open('temp.txt', 'w', encoding='UTF-8', errors='ignore') # writing data to a new file changing the first delimiter only
with open('posts_info.txt', encoding='UTF-8', errors='ignore') as f:
    for line in f:
        line = line.replace(':', '|', 1) # only replace first instance of : to use this as delimiter for pandas
        new_temp.write(line)
new_temp.close()

df = pd.read_csv('temp.txt', delimiter='|', header=None, encoding='UTF-8')
df = df.set_index([0]).T
df.to_csv('./new_transposed_df.csv', index=False)