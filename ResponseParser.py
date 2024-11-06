import json

class ResponseParser:
   def __init__(self):
      self.arr = list()
      self.res = list()
      self.indx = 0

   def check_valid_str(self, j):
      sz = len(j)
      self.indx = 0

      if sz == 0:
         return 0

      if len(self.res) > 0 and j[self.indx] == '{' and self.res[len(self.res) -1][0] == '{':
         self.res.clear()
      elif j[self.indx] != '{':
         e = str(j).find('}', self.indx)
         if e > 0 and len(self.res) > 0:
            self.arr.append(self.res.pop(len(self.res) -1) + j[self.indx:e + 1:1])
            self.res.clear()
            self.indx += e + 1

      return sz

   def parse(self, j):
      sz = self.check_valid_str(j)

      while sz > self.indx and self.indx >= 0:
         e = str(j).find('}', self.indx)
         if e > 0:
            self.arr.append(j[self.indx:e + 1:1])
         elif self.indx >= 0:
            s = j[self.indx:sz:1]
            self.res.append(j[self.indx:sz:1])
            return

         self.indx += e + 1
      pass

   # def get_strings(self):
   #    for s in self.arr:
   #       self.parse(s)

