__author__ = 'fissalalsharef'

# from BeautifulSoup import *
from urllib2 import *
from Tkinter import *
from urlparse import urljoin
from docclass import *
import ttk



class BookFetcheerApp():
    def __init__(self):
        self.data1 = {}
        self.data2 = []

        self.InterFace()

    def opening_url_and_making_soup(self,url):
            request = Request(url)
            response = urlopen(request)
            html_version = response.read()
            soup = BeautifulSoup(html_version)

            return soup

    def set(self):
        dep = self.box2.get()
        threshold = self.entry2.get()
        if dep not in self.data1:
            self.data1.setdefault(dep,threshold)
            self.data2.append(dep)
        else:
            self.data1[dep] = threshold
        self.listbox.delete(0,END)
        for i in self.data2:
            self.listbox.insert(END,'%s %s\n'%(str(i),str(self.data1[i])))


    def remove(self):
        self.items = self.listbox.curselection()
        for i in self.items:
            self.listbox.delete(i)
            del self.data1[self.data2[i]]
            del self.data2[i]


    def fetcher(self):
        global dict_of_categories_and_links
        global dict_of_bookname
        global cat_and_bookname
        global list_of_categories
        global dict_of_book_and_cat
        list_of_categories = []
        list_of_all_books_links = []
        dict_of_bookname = {}
        dict_of_categories_and_links = {}
        cat_and_bookname = {}
        lis_of_cat = []
        list_of_books=[]
        dict_of_book_and_cat = {}
        try:
            link = self.entry.get()
            if len(link) == 0:
                    self.Error_Message()
            soup = self.opening_url_and_making_soup(link)

            for i in soup.fetch('a'):
                if ('class' in dict(i.attrs)) and (i['class'] == "category_box"):
                    new_url  = urljoin(link,i['href'])
                    split = new_url.split("/")
                    cat = split[4]
                    new_soup = self.opening_url_and_making_soup(new_url)
                    lis_of_cat.append(split[4])
                    for j in new_soup.fetch('a'):
                        if ('class' in dict(j.attrs)) and (j['class'] == "doc_link book_link"):
                            url_of_books  = urljoin(link,j['href'])
                            list_of_all_books_links.append(url_of_books)
                            dict_of_categories_and_links.setdefault(cat,[])
                            dict_of_categories_and_links[cat].append(url_of_books)

            for cat1 in lis_of_cat:
                self.text.insert(END,'%s (Pending)\n'% cat1)
                self.root.update_idletasks()

            v = 0
            for key in dict_of_categories_and_links:
                r = float(v+1)
                self.text.delete(r,r+1)
                self.text.insert(r,'%s (In Progress)\n'%lis_of_cat[v])
                self.text.update()
                for i in range(2):
                    new_soup1 = self.opening_url_and_making_soup(dict_of_categories_and_links[key][i])
                    split = dict_of_categories_and_links[key][i].split("/")
                    cat_and_bookname.setdefault(key, [])
                    cat_and_bookname[key].append(split[5])
                    list_of_books.append(split[5])
                    for ii in new_soup1.fetch('div'):
                        if ('class' in dict(ii.attrs)) and (ii['class'] == "description"):
                            all_text = ''.join(ii.findAll(text=True))
                            dict_of_bookname.setdefault(str(split[5]), all_text)
                            dict_of_book_and_cat.setdefault(split[5],key)
                    self.text.delete(r,r+1)
                    self.text.insert(r,'%s (Complete)\n'%lis_of_cat[v])
                list_of_categories.append(key)

                v +=1
            self.box['values']=tuple(list_of_books)
            self.box2['values']=tuple(lis_of_cat)
        except:
            pass


    def Train_The_Algorithm(self,v):
        book = self.box.get()
        for name in dict_of_bookname:
            if name != book:
                v.train(dict_of_bookname[name],dict_of_book_and_cat[name])
            else:
                pass

    def Guess_The_Category(self):
        book = self.box.get()
        if self.P.get() == 0:
            v = naivebayes(getwords)
            self.Train_The_Algorithm(v)
            for dep in list_of_categories:
                v.setthreshold(dep,1.0)
            try:
                for t in self.data1:
                    dep,threshold = t,self.data1[t]
                    v.setthreshold(dep,threshold)
                self.out = v.classify(dict_of_bookname[book],default='unknown')
            except:
                self.out = 'unknown'
        else:
            v = fisherclassifier(getwords)
            self.Train_The_Algorithm(v)
            for dep in list_of_categories:
                v.setminimum(dep,0.0)
            try:
                for t in self.data1:
                    dep,threshold = t,self.data1[t]
                self.out = v.classify(dict_of_bookname[book],default='unknown')
            except:
                self.out = 'unknown'


        if self.out == dict_of_book_and_cat[book]:
            self.label_7.config(text = '%s'%str(dict_of_book_and_cat[book]),fg = 'red',bg = 'spring green')
        else:
            self.label_7.config(text = '%s  Correct Answer: %s'%(self.out,str(dict_of_book_and_cat[book])),fg = 'spring green',bg = 'red')

    def Error_Message(self):
        error_Window = Toplevel()
        error_Massage = Label(error_Window,text = """Please Insert the URLs\nand fetch the data first""",font="Times 40 bold",fg = "red", bg = "black")
        error_Massage.pack()

    def InterFace(self):
        
        self.root = Tk()
        self.root['bg'] = 'black'
        self.root.title('Guess My book category')
        self.root.geometry('900x700+200+10')
        self.link = StringVar()
        self.P = IntVar()
        self.threshold = IntVar()
        self.label_1 = Label(self.root,text = 'Guess Book Category', padx = 100, pady = 30,font=("Helvetica", 20),fg = "white smoke",bg = 'gray')
        self.label_1.pack(padx = 5,pady = 5,fill = BOTH)
        self.label_2 = Label(self.root, text = 'Provide book site URL: ',font=("Helvetica", 12),fg = 'white smoke',bg = 'dark grey')
        self.label_2.pack()
        self.entry = Entry(self.root,textvariable = self.link)
        self.entry.pack(padx = 10,pady = 10,fill = BOTH)
        self.button1 = Button(self.root,text = 'Fetch book information',command = self.fetcher,height = 1,fg = 'white smoke',bg = 'black',font=("Helvetica", 12))
        self.button1.pack(padx = 5,pady = 5)
        self.frame1 = Frame()
        self.frame1.pack()
        self.scroll = Scrollbar(self.frame1)
        self.scroll.pack(side = RIGHT,fill = Y)
        self.text = Text(self.frame1,width = 100,height = 8,yscrollcommand=self.scroll)
        self.text.pack()
        self.frame2 = Frame(bg='dark grey')
        self.frame2.pack()
        self.frame3 = Frame(bg='dark grey')
        self.frame3.grid(row=0, column=0,padx=20,in_=self.frame2)
        self.frame4 = Frame(bg='dark grey')
        self.frame4.grid(row=0, column=1,padx=20,in_=self.frame2)
        self.label_3 = Label(self.frame3, text = 'Choose The Classification Method:',font=("Helvetica", 12),fg = 'blue',bg = 'dark grey')
        self.label_3.grid(row = 0,column = 0)
        self.frame5 = Frame(bg='dark grey')
        self.frame5.grid(row=0, column=1,padx=20,pady = 30,in_=self.frame3)
        self.radio1 = Radiobutton(self.frame5,text = 'Naive Bayes',variable = self.P,value = 0,bg = 'dark grey')
        self.radio1.grid(sticky = W,row = 0, column = 0)
        self.radio1 = Radiobutton(self.frame5,text = 'Fisher',variable = self.P,value = 1,bg = 'dark grey')
        self.radio1.grid(sticky = W,row = 1, column = 0)
        self.label_4 = Label(self.frame3,text = 'Select a book:',font=("Helvetica", 12),fg = 'blue',bg = 'dark grey')
        self.label_4.grid(row = 1,column = 0)
        self.box = ttk.Combobox(self.frame3)
        self.box.grid(row = 1,column = 1)
        self.label_5 = Label(self.frame4,text = 'Set the Threshold:',font=("Helvetica", 12),fg = 'blue',bg = 'dark grey')
        self.label_5.grid(padx = 10,pady = 10)
        self.listbox = Listbox(self.frame4,width = 30,height = 5)
        self.listbox.grid()
        self.button2 = Button(self.frame4,text = 'Remove Selected',command = self.remove,height = 1,fg = 'white smoke',bg = 'black',font=("Helvetica", 10))
        self.button2.grid(row = 1,column = 1,padx = 10,pady = 10)
        self.box2 = ttk.Combobox(self.frame4)
        self.box2.grid(row = 2,column = 0)
        self.entry2 = Entry(self.frame4,textvariable = self.threshold,width = 4)
        self.entry2.grid(row = 2,column = 1,padx = 10,pady = 10)
        self.button3 = Button(self.frame4,text = 'Set',command = self.set,height = 1,fg = 'white smoke',bg = 'black',font=("Helvetica", 10))
        self.button3.grid(row = 2,column = 2)
        self.frame6 = Frame(bg='dark grey')
        self.frame6.pack()
        self.button4 = Button(self.frame6,text = 'Guess The cat of the selected book',command = self.Guess_The_Category,height = 1,fg = 'white smoke',bg = 'black',font=("Helvetica", 12))
        self.button4.grid(padx = 10,pady = 10,row = 0,column = 0)
        self.label_6 = Label(self.frame6,text = 'Predicted cat:',height = 1,font=("Helvetica", 12),fg = 'blue',bg = 'dark grey')
        self.label_6.grid(padx = 10,pady = 10,row = 1,column = 0)
        self.label_7 = Label(self.frame6,height = 1,font=("Helvetica", 12))
        self.label_7.grid(padx = 10,pady = 10,row = 2,column = 0)
        mainloop()



a = BookFetcheerApp()




