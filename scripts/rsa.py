import random 


def gcd(a,b):
	if b == 0:
		return a
	return gcd(b,a%b)

def prime_finder():
	test_number = random.randrange(10,100)
	for i in range (2,test_number):
		if test_number % i == 0:
			return prime_finder()
	return test_number

if __name__ == '__main__':
	p=prime_finder()
	q=prime_finder()
	n = p * q
	phi = (p-1) * (q-1)
	
	print('p: '+str(p),'q: '+str(q),'n: '+str(n),'phi: '+str(phi))

	pub_keys= []
	for i in range (2,phi):
		if gcd(i,phi)== 1 and gcd (i,n) == 1:
			pub_keys.append(i)
		if len(pub_keys) >= 100:
			break
	e = random.choice(pub_keys)
	del(pub_keys)
	
	priv_keys = []
	i = 2
	while len(priv_keys) < 5:
	    if i * e % phi == 1:
	    	print(i)
	    	priv_keys.append(i)
	    i += 1
	d = random.choice(priv_keys)
	del(priv_keys)

	print(f"Public Key: ({e}, {n})\nPrivate Key: ({d}, {n})")
