from collections import Counter


s = 'abba'

# count = 0
# arr = []

# dic = Counter(s)

# for i in dic:
#   if dic[i] % 2 == 0:
#     count += (dic[i]//2)
#     arr.append(i)


# print(Counter(s))
# print(count)

sum = 0
for i, el in enumerate(s):
  j = 1
  B = Counter(s[i+1:])
  while j < len(s):
    A = Counter(el)
    print('el: ' + el)
    print(A)
    print(B)
    print(A-B)
    if A - B == {}:
      sum +=1
      print('sum: ' + str(sum))
    j += 1
    el = "".join(s[i:j])


# print(Counter(i) - Counter(s[s.index(i)+1:]))

print(sum)