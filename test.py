
from datetime import time



DAYS =[
    (1,('Monday')),
    (2,('Tuesday')),
    (3,('Wednesday')),
    (4,('Thursday')),
    (5,('Friday')),
    (6,('Saturday')),
    (7,('Sunday')),

]



# HOURS_OF_DAY_24 = [(time(hr, m).strftime('%I:%M: %p'),time(hr, m).strftime('%I:%M: %p')) for hr in range(1,24) for m in range(0,30)]

HOURS_OF_DAY_24 = [
    (time(hr, m).strftime('%I:%M %p'), time(hr, m).strftime('%I:%M %p')) 
    for hr in range(0, 24) for m in (0, 30)
]




