import schedule
import time
from datetime import datetime

def ku():
    hour = datetime.now().hour
    print("Ку " * min(hour, 12))

schedule.every().hour.at(":00").do(ku)

while True:
    schedule.run_pending()
    time.sleep(1)
