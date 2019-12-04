# Just because it seems like the Python solution can be _even_ sillier
from functools import reduce

def verify_number(num):
    if sorted(str(num)) != list(str(num)):
        return False
    
    counts = []
    count = 1
    last = str(num)[0]
    for n in str(num)[1:]:
        if n == last:
            count += 1
        else:
            counts.append(count)
            count = 1
            last = n
    counts.append(count)

    return 2 in counts

start = 245318
end = 765747

count = 0

for n in range(start, end + 1):
    if verify_number(n):
        count += 1

print(count)