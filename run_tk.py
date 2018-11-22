from tkinter.ttk import Button,Entry,Radiobutton,Scrollbar
from tkinter import END,Label,Tk,StringVar,Listbox,messagebox,SINGLE,PhotoImage
from 爱奇艺_project.movie_get import Pro
from PIL import Image,ImageTk
import io
import re
import requests
# from urllib.request import urlopen

class Movie_app:
    def __init__(self):
        self.win=Tk()
        self.win.geometry('600x420')
        self.win.title("爱奇艺-优酷-PPTV视频播放下载器V3.1")
        self.creat_res()
        self.creat_radiores()
        self.config()
        self.page=1
        self.p=Pro()
        self.win.mainloop()


    def creat_res(self):
        self.temp=StringVar()#url地址
        self.temp2=StringVar()
        self.t1=StringVar()#通道
        self.t3=StringVar()#爱奇艺，优酷，PPTV
        self.La_title=Label(self.win,text="地址:")
        self.La_way=Label(self.win,text="选择视频通道:")
        self.R_way1=Radiobutton(self.win,text="通道A",variable=self.t1,value=True)
        self.R_way2=Radiobutton(self.win,text="通道B",variable=self.t1,value=False)
        self.R_aiqiyi=Radiobutton(self.win,text="爱奇艺",variable=self.t3,value="a")
        self.R_youku=Radiobutton(self.win,text="优酷",variable=self.t3,value="y")
        self.R_pptv=Radiobutton(self.win,text="PPTV",variable=self.t3,value="p")
        self.B_play=Button(self.win,text="播放▶")
        self.B_uppage=Button(self.win,text="上页")
        self.B_nextpage=Button(self.win,text="下页")
        self.B_search=Button(self.win,text="♣搜索全站♠")
        self.La_mesasge=Label(self.win,text="☜  ⇠☸⇢  ☞",bg="pink")
        self.La_page=Label(self.win,bg="#BFEFFF")
        self.S_croll=Scrollbar(self.win)
        self.L_box=Listbox(self.win,bg="#BFEFFF",selectmode=SINGLE)
        self.E_address=Entry(self.win,textvariable=self.temp)
        self.La_title.place(x=10,y=50,width=50,height=30)
        self.E_address.place(x=70,y=50,width=200,height=30)
        self.B_play.place(x=300,y=50,width=50,height=30)
        self.R_way1.place(x=160,y=10,width=70,height=30)
        self.R_way2.place(x=240,y=10,width=70,height=30)
        self.La_way.place(x=10,y=10,width=100,height=30)
        self.R_aiqiyi.place(x=20,y=100,width=70,height=30)
        self.R_youku.place(x=90,y=100,width=70,height=30)
        self.R_pptv.place(x=160,y=100,width=70,height=30)
        self.B_search.place(x=252,y=140,width=100,height=30)
        self.La_mesasge.place(x=80,y=125,width=90,height=20)
        self.L_box.place(x=10,y=180,width=252,height=230)
        self.S_croll.place(x=260,y=180,width=20,height=230)
        self.B_uppage.place(x=10,y=140,width=50,height=30)
        self.B_nextpage.place(x=180,y=140,width=50,height=30)
        self.La_page.place(x=80,y=150,width=90,height=28)

    def creat_radiores(self):
        self.movie=StringVar()#电影
        self.S_croll2=Scrollbar()#分集
        self.La_pic=Label(self.win,bg="#E6E6FA")
        self.La_movie_message=Listbox(self.win,bg="#7EC0EE")
        self.R_movie=Radiobutton(self.win,text="电影",variable=self.movie,value="m")
        self.tv=Radiobutton(self.win,text="电视剧",variable=self.movie,value="t")
        self.zhongyi=Radiobutton(self.win,text="综艺",variable=self.movie,value="z")
        self.dongman=Radiobutton(self.win,text="动漫",variable=self.movie,value="d")
        self.jilupian=Radiobutton(self.win,text="纪录片",variable=self.movie,value="j")
        self.B_view=Button(self.win,text="✤查看✤")
        self.B_info=Button(self.win,text="使用说明")
        self.B_clearbox=Button(self.win,text="清空列表")
        self.B_add=Button(self.win,text="添加到播放列表")
        self.R_movie.place(x=290,y=180,width=80,height=30)
        self.B_view.place(x=290,y=330,width=70,height=30)
        self.B_add.place(x=370,y=255,width=100,height=30)
        self.B_clearbox.place(x=500,y=255,width=70,height=30)
        self.tv.place(x=290,y=210,width=80,height=30)
        self.zhongyi.place(x=290,y=240,width=80,height=30)
        self.dongman.place(x=290,y=270,width=80,height=30)
        self.jilupian.place(x=290,y=300,width=80,height=30)
        self.La_movie_message.place(x=370,y=290,width=200,height=120)
        self.La_pic.place(x=370,y=10,width=200,height=240)
        self.B_info.place(x=290,y=370,width=70,height=30)
        self.S_croll2.place(x=568,y=290,width=20,height=120)

    def show_info(self):
        msg="""
        1.输入视频播放地址，即可播放
          选择A或者B可切换视频源
        2.选择视频网，选择电视剧或者电影，
          搜索全网后选择想要看得影片，点
          查看，在右方list里选择分集视频
          添加到播放列表里点选播放
        """
        messagebox.showinfo(title="使用说明",message=msg)

    def config(self):
        self.t1.set(True)
        self.B_play.config(command=self.play_url_movie)
        self.B_search.config(command=self.search_full_movie)
        self.B_info.config(command=self.show_info)
        self.S_croll.config(command=self.L_box.yview)
        self.L_box['yscrollcommand']=self.S_croll.set
        self.S_croll2.config(command=self.La_movie_message.yview)
        self.La_movie_message['yscrollcommand']=self.S_croll2.set
        self.B_view.config(command=self.view_movies)
        self.B_add.config(command=self.add_play_list)
        self.B_clearbox.config(command=self.clear_lisbox2)
        self.B_uppage.config(command=self.uppage_)
        self.B_nextpage.config(command=self.nextpage_)

    def uppage_(self):
        print('---------上一页---------')
        self.page-=1
        print(self.page)
        if self.page<1:
            self.page=1

    def nextpage_(self):
        print('----------下一页--------')
        self.page+=1
        print(self.page)
        if self.t3=="a" or self.t3=="y":
            if self.page>30:
                self.page=30
        elif self.t3=="p":
            if self.movie=="m":
                if self.page>165:
                    self.page=165
            elif self.movie == "t":
                if self.page > 85:
                    self.page = 85
            elif self.movie == "z":
                if self.page > 38:
                    self.page = 38
            elif self.movie == "d":
                if self.page > 146:
                    self.page = 146
            elif self.movie == "j":
                if self.page > 40:
                    self.page = 40

    def clear_lisbox(self):
        self.L_box.delete(0,END)

    def clear_lisbox2(self):
        self.La_movie_message.delete(0,END)

    def search_full_movie(self):
        print("-----search----")
        self.La_page.config(text="当前页:{}".format(self.page))
        self.clear_lisbox()
        try:
            movie_url, movie_title, movie_src_pic=self.p.get_movie_res(self.t3.get(),self.movie.get(),self.page)
            self.movie_dic={}
            for i,j,k in zip(movie_title,movie_url,movie_src_pic):
                self.movie_dic[i]=[j,k]
            for title in movie_title:
                self.L_box.insert(END,title)
            print(self.movie_dic)
            return self.movie_dic
        except:
            messagebox.showerror(title='警告',message='请选择电影或者电视剧')

    def add_play_list(self):
        print('---------playlist----------')
        print(self.movie_dic)
        if self.La_movie_message.get(self.La_movie_message.curselection())=="":
            messagebox.showwarning(title="警告",message='请在列表选择影片')
        else:
            print("电影名字:",self.La_movie_message.get(self.La_movie_message.curselection()))
            if self.movie.get()!="m":
                self.temp.set(self.new_more_dic[self.La_movie_message.get(self.La_movie_message.curselection())])
            else:
                self.temp.set(self.movie_dic[self.La_movie_message.get(self.La_movie_message.curselection())][0])


    def view_pic(self,pic_url):
        print('--------viewpic---------')
        pa_url_check=r'//.+[.]jpg'
        if re.match(pa_url_check,pic_url):
            print("ok")
            pic_url="http:"+pic_url
        print(pic_url)
        data=requests.get(pic_url).content
        # data=urlopen(pic_url).read()
        io_data=io.BytesIO(data)
        self.img=Image.open(io_data)
        self.u=ImageTk.PhotoImage(self.img)
        self.La_pic.config(image=self.u)

    def view_movies(self):
        print("--------viewmovie----------")
        cur_index=self.L_box.curselection()
        print(self.L_box.get(cur_index))
        if self.movie.get()!="m":#非电影类
            self.new_more_dic=self.p.get_more_tv_urls(self.movie_dic[self.L_box.get(cur_index)][0],self.t3.get(),self.movie.get())
            print(self.new_more_dic)
            for i,fenji_url in self.new_more_dic.items():
                self.La_movie_message.insert(END, i)
        else:#电影类
            self.La_movie_message.insert(END,self.L_box.get(cur_index))
        self.view_pic(self.movie_dic[self.L_box.get(self.L_box.curselection())][1])#加载图片

    def play_url_movie(self):
        print("--------ok-----------")
        # print(type(self.t1.get()),self.t1.get())
        if self.temp.get()=="":
            messagebox.showwarning(title="警告",message="请先输入视频地址")
        else:
            if self.t1.get()!="":
                self.p.play_movie(self.temp.get(),self.t1.get())
            else:
                messagebox.showwarning(title='警告',message='请选择通道')


m=Movie_app()
