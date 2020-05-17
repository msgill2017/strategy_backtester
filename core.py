from commons import open_file, trading_days, order_place

symbol = 'DLF'
expiry_date = '30-05-2019'

optionchain_df = open_file("Data/{}-OPTSTK-{}.csv".format(symbol, expiry_date))

working_days = trading_days(optionchain_df)

# print(optionchain_df)
# print(working_days)
for day in working_days:
    print("Today is Date:{}".format(day))
    filter_date = optionchain_df['Date'] == day
    current_day_optionchain_df = optionchain_df[filter_date]
    # print(current_day_optionchain_df)
    while True:
        order = []
        trade = input("Are you interested in Trade Today (Yes or No):")
        if trade == '' or trade[0].upper() == 'Y':
            order = order_place(day, current_day_optionchain_df)
        #     orders_list.append(order)
        #     # print("Order List", len(orders_list))
        #     display_trade_info(orders_list)

        if trade and trade[0].upper() != 'Y':
            # if orders_lst:
                # display_trade_info(orders_list)
            # else:
            print("----------------------------------")
            print("No trade is available to display yet")
            break

