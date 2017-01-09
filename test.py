__author__ = 'fissalalsharef'

# import re
#
# mystring = '<h1 id="newsTitle">A dangerous gambit in northern Syria</h1>'
# pattern = re.compile("^(<.*>)(.*)(<.*>)$",re.VERBOSE)
# newstring = pattern.sub(r"\1'\2' ", mystring)
# print pattern.match(mystring).group(2)
# import nltk
# from nltk.corpus import stopwords
# s=set(stopwords.words('english'))
#
# txt="there is a lot of stuff to be disscused who are the fuck are you there who while others are commercial or proprietary"
# s = filter(lambda w: not w in s,txt.split())
#
# print s
# def lazy_stopword_filter(filename):
#     print "Sd"
#     with open(filename) as text:
#         print "sd"
#         for line in text:
#             print line
#             for word in line.split(): # simple tokenization
#                 if word not in stopwords.words('english'):
#                     yield word
#
#
# lazy_stopword_filter("Will_be_Cluestered.txt")
#
# word_list = "The security researchers who found the flaw in OpenSSL package named it the heartbleed bug. It works like this: Another OpenSSL-installed computer connects to your computer and tricks your computer to send some memory blocks to it. Unfortunately, the memory block will contain sensitive data, particularly encryption keys and passwords. The OpenSSL team fixed the software and published the new version within the same day. Does this mean the problem is over? Far from it."
# filtered_words = [w for w in word_list if not w in stopwords.words('english')]
# print filtered_words

# s = open("Will_be_Cluestered.txt").read()
# # tokens = nltk.word_tokenize(s)
# def cleanupDoc(s):
#     stopset = set(stopwords.words('english'))
#     tokens = nltk.word_tokenize(s)
#     cleanup = []
#     for token in tokens:
#         if token not in stopset and len(token)>3:
#             cleanup.append(token.lower())
#
#     print cleanup
#
# cleanupDoc(s)

#
# dic = {"a":1,"b":2}
# dic1 = {"a":1,"bb":3}
# for i in dic:
#     if i in dic1:
#         print i


# s = [['fissal','alsharef'],['rateb','altal']]
# ss = ['fissal','rateb']
# l = []
# for i in s:
#     for inx in i:
#         if inx in ss:
#             a = " ".join(str(x) for x in i)
#             l.append(a)
# print l

# from BeautifulSoup import *
# from urllib2 import *
# from Tkinter import *
# from urlparse import urljoin
# import miniProjects.MiniProjects_2.clusters
# from miniProjects.MiniProjects_2.clusters import *
# from nltk.corpus import stopwords
# import nltk

#
# def opening_url_and_making_soup(url):
#             request = Request(url)
#             response = urlopen(request)
#             html_version = response.read()
#             soup = BeautifulSoup(html_version)
#             return soup
#
# def fetch(link):
#     s = opening_url_and_making_soup(link)
#     print (s)
#
#
#
# link = "http://www.barnesandnoble.com/b/books/fiction/_/N-29Z8q8Z10h8"
# fetch(link)

# a = "http://www.barnesandnoble.com/b/books/computers/_/N-29Z8q8Zug4"
# b = a.split("/")
# print len(b)
# import urllib3
# http = urllib3.PoolManager(10)
# r1 = http.request('GET', 'http://www.barnesandnoble.com/b/books/sports/_/N-29Z8q8Z19id')
#
# s = BeautifulSoup(r1)
# print s

from BeautifulSoup import *
from urllib2 import *
from Tkinter import *
from urlparse import urljoin


Categories = ["sports", "fiction", "psychology", "computers", "education", "social-sciences"]

class BookFetcheerApp():
    def __init__(self):
        pass

    def opening_url_and_making_soup(self,url):
            request = Request(url)
            response = urlopen(request)
            html_version = response.read()
            soup = BeautifulSoup(html_version)

            return soup

    def Fetch(self, link):
        list_of_sublinks = []
        list_of_sublinks1 = []
        list_of_bookURL = []
        soup = self.opening_url_and_making_soup(link)
        print "fsf"
        for i in soup.fetch('a'):
            split = i["href"].split("/")
            for ii in Categories:
                if ii in split:
                    list_of_sublinks.append(urljoin(link,i['href']))

        for ii in list_of_sublinks:
            split = ii.split("/")
            if split[-1][0:5] == "N-29Z" and len(split)<=8 :
                if ii not in list_of_sublinks1:
                    list_of_sublinks1.append(ii)
                    new_url = self.opening_url_and_making_soup(ii)
                    print new_url
        #             for j in new_url.fetch('a'):
        #                 if ('class' in dict(j.attrs)) and (j['class'] == "carousel-image-link"):
        #                     new_url  = urljoin(ii,j['href'])
        #                     list_of_bookURL.append(new_url)
        #
        #
        #
        #
        #
        # print list_of_bookURL

link = "http://www.barnesandnoble.com/h/books/browse"
a = BookFetcheerApp()
s = a.Fetch(link)
print s