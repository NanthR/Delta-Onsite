from string import ascii_letters, digits
from itertools import product

password = "wlhE8tAhKc859Gu"
check = "wlhEXtAhKcXY"

choices = ascii_letters + digits

count = 0

flag = 0

while True:
	print(count)
	for i in product(choices, repeat=count):
		for j in range(9):
			for k in range(9):
				temp = check
				temp = temp.replace('X', str(j))
				temp = temp.replace('Y', str(k))
				temp += ''.join(l for l in i)
				# print(temp)
				if temp == password:
					print(temp)
					flag = 1
					break
			if flag == 1:
				break
		if flag == 1:
			break
	if flag == 1:
			break
					
	count += 1