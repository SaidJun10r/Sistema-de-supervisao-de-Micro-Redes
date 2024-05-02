def is_leap(year):
    leap = False
    
    if year//4 == 0:
        leap = True
        if year//100 != 0:
            leap = False
        else:
            leap = True
            if year//400 == 0:
                leap = True
            else:
                leap = False
    else:
        leap = False
    
    return leap

print(2400//4)
year = int(input())
print(is_leap(year))