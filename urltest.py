# from urllib.request import urlopen
import urllib.request
import urllib.error

myURL = urllib.request.urlopen("https://www.runoob.com/")
print(myURL.getcode())
