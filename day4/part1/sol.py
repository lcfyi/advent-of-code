# Just because it seems like the Python solution can be _even_ sillier

def verify_number(num):
    if sorted(str(num)) != list(str(num)):
        return False
    
    count = 1
    last = str(num)[0]
    for n in str(num)[1:]:
        if n == last:
            count += 1
        else:
            if count >= 2:
                return True
            count = 1
            last = n
    return count >= 2

start = 245318
end = 765747

count = 0

for n in range(start, end + 1):
    if verify_number(n):
        count += 1

print(count)