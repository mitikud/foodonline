from datetime import time

# for hr in range(1,24):
#     for m in range(0,30):
#         print(time(hr, m).strftime('%I:%M: %p'))

t = [(time(hr, m).strftime('%I:%M: %p'),time(hr, m).strftime('%I:%M: %p')) for hr in range(1,24) for m in range(0,30)]
print(t)