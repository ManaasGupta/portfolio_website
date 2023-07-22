from datetime import date
import calendar
today=date.today()
month=today.month
month_name=calendar.month_name[month]
print(today)
print(month)
print(month_name)