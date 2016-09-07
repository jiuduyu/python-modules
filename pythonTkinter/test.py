# -*- coding: UTF-8 -*-


from Tkinter import *           # 导入 Tkinter 库
import tkMessageBox
import FileDialog
from data import *


class Test(object):
    mainFrame = Tk()
    msg = tkMessageBox
    alert = '友情提示'
    contentName = StringVar()
    contentPwd = StringVar()
    contentTable = StringVar()
    contentHost = StringVar()

    def __init__(self, **arg):
        pass

    @staticmethod
    def eventAction():
        db = Db(host=Test.contentHost.get(), user=Test.contentName.get(),
                password=Test.contentPwd.get(), dbbase=Test.contentTable.get())
        if db.ifConnectEoor():

            Test.msg.showinfo(Test.alert, db.ifConnectEoor())
        else:
            mylist = Listbox(Test.mainFrame, width=40)
            for line in db.queryAction('SHOW TABLES'):
                mylist.insert(END, "表名: " + str(line[0]))
            mylist.pack(side=LEFT, fill=BOTH)

    @staticmethod
    def createEntryAction(show=None, bd=2):
        return Entry(Test.mainFrame, show=show, bd=bd)

    @staticmethod
    def startAction(title, width=300, height=200):
        Test.mainFrame.title(title)
        # Test.mainFrame.maxsize(width, height)
        Test.mainFrame.minsize(width, height)
        frame = Frame(Test.mainFrame)
        # left
        frameLeft = Frame(frame)
        Label(frameLeft, text="地  址", font=("Arial", 12)).pack(side=TOP)  # 左上
        Label(frameLeft, text="用户名", font=("Arial", 12)).pack(side=TOP)  # 左上

        Label(frameLeft, text="密   码", font=("Arial", 12)).pack(side=TOP)  # 左下
        Label(frameLeft, text="数据库", font=("Arial", 12)).pack(side=TOP)  # 左下
        Label(frameLeft, text="   ", font=("Arial", 12)).pack(side=TOP)  # 左下
        frameLeft.pack(side=LEFT)
        # right
        frameRight = Frame(frame)
        Entry(frameRight, bd=2, textvariable=Test.contentHost).pack(side=TOP)  # 右上
        Entry(frameRight, bd=2, textvariable=Test.contentName).pack(side=TOP)  # 右上

        Entry(frameRight, show='*', bd=2,
              textvariable=Test.contentPwd).pack(side=TOP)  # 右下
        Entry(frameRight, bd=2,
              textvariable=Test.contentTable).pack(side=TOP)  # 右下
        Button(frameRight, text='连   接',
               command=Test.eventAction).pack(side=BOTTOM)
        frameRight.pack(side=RIGHT)

        frame.pack()
        Test.mainFrame.mainloop()

Test.startAction('数据库测试.')
