from commons import open_file, trading_days

symbol = 'DLF'
expiry_date = '30-05-2019'

optionchain_df = open_file("Data/{}-FUTSTK-{}.csv".format(symbol,expiry_date))

working_days = trading_days(optionchain_df)

# print(optionchain_df)
print(working_days)
