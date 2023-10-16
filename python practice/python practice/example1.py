# # arr = input("Enter array elements\n").split();
# # arr = [int(num) for num in arr]
# # i=9;
# # while(len(arr)>0):
# #     print(arr[i]);
# #     i--
# from os import remove
#
s = input("Enter the string\n")
r = ['a', 'e', 'i', 'o', 'u']
t = ""
for i in s:
    if i in r:
        continue
    t = t + i
print(t)
