from string import ascii_letters, digits
from itertools import product
import threading
from os import _exit

password = "wlhE8tAhKc85aaaaaa"
check = "wlhEXtAhKcXY"

choices = ascii_letters + digits

def passCheck(count):
	flag = 0
	for i in product(choices, repeat=count):
		for j in range(10):
			for k in range(10):
				temp = check
				temp = temp.replace('X', str(j))
				temp = temp.replace('Y', str(k))
				temp += ''.join(l for l in i)
				if temp == password:
					print(temp)
					flag = 1
					break
			if flag == 1:
				break
		if flag == 1:
			break
	if flag == 1:
			_exit(0)
					
if __name__ == "__main__":
	i = 0
	max_threads = 8
	for i in range(max_threads):
		t = threading.Thread(target=passCheck, args=(i,))
		t.start()
		i += 1
