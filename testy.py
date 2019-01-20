import time

current_time = time.strftime("%Y-%m-%d")
curr_day = int(time.strftime("%d"))
curr_month = int(time.strftime("%m"))
curr_year = int(time.strftime("%Y"))

dates_list = []

for i in range(curr_day, curr_day + 5):
    if i > 31:
        dates_list.append([str(curr_year) + '-0' + str(curr_month + 1) + '-' + str(i-31)])
    else:
        dates_list.append([str(curr_year) + '-0' + str(curr_month) + "-" + str(i)])

print(dates_list)
