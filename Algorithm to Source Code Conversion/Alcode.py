from Tkinter import *
import tkMessageBox
import tkFileDialog

data = list()

root = Tk() #root the name given to the entire window
root.configure(background = 'light sea green')
label1 = Label(root,text="Automated Algorithm to Source Code Conversion",fg = "white",bg = 'light sea green',font=("Helvetica", 35))
label1.pack(anchor = CENTER)
d = ''
flag = 0
file_path = ''
a = ''
def callBack(): #callback function to restore the state of the text area
    textArea.configure(state="normal")
    global flag
    flag = 1
    


def process():

    if(flag==1):
        global d
        text = textArea.get("1.0","end")    #to fetch the contents of the text area
        d = text.encode('ascii','ignore')
       
    if flag == 0:
        with open(file_path) as f:
            d=f.read()
    textArea1.configure(state="normal")
    global a
    a=d.split('\n')
    count = 0
    variab = 'variablename'  
    inp=['integers', 'integer', 'number', 'numbers'] #input probabilities list
    for i in a:
            j=i.split(' ')
            for x in j:
                    if re.match(r'//Input:', x):
                            l = j
                            break
    for i in range(0, len(l)):
            if l[i] in inp:
                    for j in range(i, len(l)):
                            if len(l[j]) == 1:
                                    variab = l[j]
                                    print l[j]+'=int(raw_input("Enter your number: "))'
                                    textArea1.insert(END,l[j]+'=int(raw_input("Enter your number: "))\n')
    arr = 'arrayname'    #to check for unique array names
    for i in a:
            if (count >= 4):
                    if re.match(r'[a-zA-Z]+\[[0-9]\].*', i):    #For array assignment
                            if (i[0] != arr):
                                    print i[0]+'= {}'
                                    arr = i[0]
                    if re.match(r'.*( mod ).*', i):
                            i=i.replace('mod','%')
                    if re.match(r'.*( or ).*', i):
                            i=i.replace('or','||')
                    if re.match(r'^[\n\t]*(while).*(do).*', i): #while statement
                            i=i.replace('do',':')
                    if re.match(r'^[\n\t]*(if).*', i): #if statement
                            if re.match(r'.*(then)', i):
                                    i=i.replace('then',':')
                            if re.match(r'.*[=].*', i):
                                    i=i.replace('=', '==')
                    if re.match(r'(else)', i):
                            i=i.replace('else', 'else:')
                    if re.match(r'endif', i):
                            i=i.replace('endif', '')
                    if re.match(r'return', i):
                            i=i.replace('return', 'print')
                            j=i.split(' ')
                            if re.match(r'.*\[+[a-zA-Z]\]+', j[1]):
                                    i=j[0]+" "+j[1].replace(variab, variab+'-1')
                    if re.match(r'^[\n\t]*(for).*', i):    #for statement
                            if re.match(r'.*(<-).*', i):
                                    i=i.replace('<-', 'in range(')
                            if re.match(r'.*(to).*', i):
                                    i=i.replace('to', ',')
                            if re.match(r'.*(do).*', i):
                                    i=i.replace('do', '):')
                    if re.match(r'.*(<-).*', i): 
                            i=i.replace('<-','=')
                    if re.match(r'^[\n\t]*(repeat until)+.*', i): #Repeat until - while
                        i=i.replace('repeat until', 'while')
                        i=i+':'
                    if re.match(r'^[\n\t]*(end loop)+.*', i):
                        continue
                    if re.match(r'^[\n\t]*(increment)+.*', i): # Increment operation
                        j=i.split(' ')
                        i=i.replace('increment '+j[1], j[1]+'+=1')
                    if re.match(r'^[\n\t]*(decrement)+.*', i): # Decrement operation
                        j=i.split(' ')
                        i=i.replace('decrement '+j[1], j[1]+'-=1')
                    if re.match(r'^[\n\t]*(print newline)+.*', i): # Newline
                        i=i.replace('newline', '\\n')
                    if re.match(r'^[\n\t]*(print space)+.*', i): # Space
                        print '        print \'\','
                        continue
                    if re.match(r'^[\n\t]*(print \*)+.*', i): #If print doesnt have more than two values outside the quote
                        j=i.split(' ')
                        i=i.replace(j[1], '\''+j[1]+'\',')
                    print i
                    textArea1.insert(END,i+"\n")
            count += 1
    textArea1.configure(state="disabled")

def execute():
    global file_path
    file_path = tkFileDialog.askopenfilename()
    textArea.configure(state="normal")
    if file_path is not '':
        tkMessageBox.showinfo( "MSG BOX","File name is : "+file_path)
    with open(file_path) as files:
        a = files.read()
        textArea.insert(END,a)
        textArea.configure(state="disabled")
       # process()
    

def proc():   
    process()

frame = Frame(root) #creation of frames on the window
frame.pack()

frame0 = Frame(root)
frame0.place(in_=frame, anchor="c", relx=.5, rely=105.5) #creates a frame within a frame
frame1 = Frame(root)
frame1.pack( side = BOTTOM )

frame11= Frame(root)
frame11.place(in_=frame1, anchor="se", relx=.2, rely=.2)
B = Button(frame0, text ="Browse", fg="white",bg = "coral",command = execute,font=("Helvetica",16),width = 15)  #button creation
B.pack(side = BOTTOM,anchor = CENTER)

frame3 = Frame(root)
frame3.pack(side = LEFT)

frame2 = Frame(root)
frame2.place(in_=frame3, anchor="c", relx=1.35, rely=.5)

B1 = Button(frame2,text = ">>",bg = "coral",fg = "white", command = proc,font=("Helvetica",16),height = 3,width = 5)
B1.pack(side = RIGHT,anchor = CENTER)

'''B2 = Button(frame2,text = ">>>>>>",bg = "coral",fg = "white", command = callBack,font=("Helvetica",16),height = 3,width = 5)
B2.pack(side = RIGHT,anchor = CENTER)'''


#B = Button(frame, text ="Close",fg="red", command = root.destroy,font="Tahoma")

#B.pack(side=RIGHT)

S = Scrollbar(frame3)   #text area with scrollbar
textArea = Text(frame3,height=10,width=60,state = DISABLED)
S.pack(side=RIGHT, fill=Y)
textArea.pack(side=LEFT, fill=Y)
S.config(command=textArea.yview)
textArea.config(yscrollcommand=S.set)


frame4 = Frame(root)
frame4.pack(side = RIGHT)
S1 = Scrollbar(frame4)
textArea1 = Text(frame4,height=10,width=60,state=DISABLED)
S1.pack(side=RIGHT, fill=Y)
textArea1.pack(side=LEFT, fill=Y)
S1.config(command=textArea.yview)
textArea1.config(yscrollcommand=S.set)
textArea.pack()

frame12 = Frame(root)   #creation of another frame with a checkbox in it
frame12.place(in_=frame3, anchor='c',relx=0.5, rely=1.5)
c = Checkbutton(frame12,text="write algorithm",font=("Helvetica",16),bg = 'light sea green',command = callBack)
c.pack(side = LEFT,anchor = CENTER)

root.mainloop()
