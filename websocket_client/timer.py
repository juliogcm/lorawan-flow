import cache
import time

def countdown(time_stamp):
    #exp = cache.expire_time
    while time_stamp:
        mins, secs = divmod(time_stamp, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        time_stamp -= 1
        #exp -= 1

        #if exp == 0:
        #    cache.expire_thread = True
        #    exp = cache.expire_time

        if (cache.stop_thread == True):
            break
    cache.time_thread = True
     