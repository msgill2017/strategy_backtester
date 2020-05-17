from commons import open_file

symbol = 'DLF'
expiry_date = '30-03-2019'

optionchain_df = open_file("Data/{}-FUTSTK-{}.csv".format(symbol,expiry_date))

print(optionchain_df)