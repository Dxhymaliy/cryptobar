import json

if __name__ == "__main__":
   j = '{"s":"BTCUSDT","i":"1s","E":1726300645006,"t":1726300639000,"T":1726300644999,"o":"60150.200000","c":"60150.200000","h":"60150.210000","l":"60150.200000","p":0.000000}'
   print(j)
   # print(j.find("}{"))
   # str1 = j[0:j.find("}{")+1:1]
   # print(str1)
   # str2 = j[j.find("}{")+1:len(j)]
   # print(str2)
   # resp = json.loads(str1)

   indx = j.find("}{")
   print(f"++++ index: {indx}")
   if indx > 0:
      str1 = j[0:indx+1:1]
      print(f"++++ receive: {str1}")
      resp = json.loads(str1)


