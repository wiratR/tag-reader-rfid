def uuid_to_decimal(uuidStr):
    resultArray = uuidStr.split(":")
    hexArray = resultArray[1].split(" ")
    # Remove multiple empty spaces from string List
    # Using list comprehension + strip()
    res = [ele for ele in hexArray if ele.strip()]
    hexStr=''
    for i in range (len(res)):
        x = len(res) - (i + 1)
        res[x]=res[x][2:]
        if len(res[x])<2:
            res[x]='0'+res[x]
        hexStr=hexStr+res[x]
    # log.debug(hexStr)
      
    c = counter = i = 0
    
    size = len(hexStr) - 1
    # loop will run till size 
    while size >= 0: 
    
        if hexStr[size] >= '0' and hexStr[size] <= '9': 
            rem = int(hexStr[size]) 
    
        elif hexStr[size] >= 'A' and hexStr[size] <= 'F': 
            rem = ord(hexStr[size]) - 55
    
        elif hexStr[size] >= 'a' and hexStr[size] <= 'f': 
            rem = ord(hexStr[size]) - 87
        else: 
            c = 1
            break
        counter = counter + (rem * (16 ** i)) 
        size = size - 1
        i = i+1
    # print("Decimal Value = ", counter) 
    return counter