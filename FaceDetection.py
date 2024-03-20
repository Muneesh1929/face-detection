from tkinter import * 
from tkinter import messagebox
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

win=Tk()
win.state("zoomed")
win.resizable(width=False, height=False)
win.configure(bg="orange")
win.title("My project")

lbl_title=Label(win,text="Face Detection",font=('',55,'bold','underline'),bg='orange')
lbl_title.place(relx=.3, rely=0)

#----------------------------------------Image---------------------------------------
imageFrame=None

def startface(frame, cv2image, lmain):
    clf=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces=clf.detectMultiScale(gray, 1.2, 5)
    for x,y,w,h in faces:
        cv2.rectangle(cv2image, (x,y), (x+w,y+h), (255,0,0), 2)

    # Resize the image to fit within the screen dimensions
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    image_height, image_width, _ = cv2image.shape
    scaling_factor = min(screen_width / (image_width * 2), screen_height / (image_height * 2))
    resized_image = cv2.resize(cv2image, (int(image_width * scaling_factor), int(image_height * scaling_factor)))

    img = Image.fromarray(resized_image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)



def browse():
    global imageFrame
    if imageFrame is not None:
        imageFrame.destroy()
    file_path=filedialog.askopenfilename()
    frame=cv2.imread(file_path)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Get screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate the size of the displayed image
    image_height, image_width, _ = cv2image.shape
    scaling_factor = min(screen_width / image_width, screen_height / image_height)
    resized_image = cv2.resize(cv2image, (int(image_width * scaling_factor), int(image_height * scaling_factor)))
    
    imageFrame = Frame(width=resized_image.shape[1], height=resized_image.shape[0], bd=6, bg='black')
    lmain = Label(imageFrame)
    lmain.grid(row=0, column=0)
    imageFrame.place(relx=.5, rely=.5, anchor="center")

    img = Image.fromarray(resized_image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)

    btn_Detection = Button(command=lambda: startface(frame, cv2image, lmain), text='Detect face', font=('',20,'bold'), bd=10, width=12).place(relx=.4,rely=.9)

def image_screen():
    frm=Frame(win, bg='sky blue')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=1)
 
    btn_Browse=Button(frm, command=lambda: browse(), text="Browse", font=('',20,'bold'), bd=10, width=8)
    btn_Browse.place(relx=.38, rely=.01)

    btn_back=Button(frm, command=lambda: welcome_screen(), text="back", font=('',20,'bold'), bd=10)
    btn_back.place(relx=.9, rely=0)

#----------------------------------------------xxxxxxxxxx-----------------------------------------------------------    


#-------------------------------------------Video_Screen--------------------------------------------------------------
iFrame=None

def browse_video():
    global iFrame
    if iFrame is not None:
        iFrame.destroy()
    file_path=filedialog.askopenfilename()
    vdo=cv2.VideoCapture(file_path)
    
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    while True:
        flag,img=vdo.read()
        if flag == True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = clf.detectMultiScale(gray, 1.4, 6)
            cv2.putText(img, "Press 'q' to quit video", (20, 30), 5, 2, (255,0,0), 2)
            for x,y,w,h in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)

            # Resize the video frame to fit within the screen dimensions
            frame_height, frame_width, _ = img.shape
            scaling_factor = min(screen_width / (frame_width * 2), screen_height / (frame_height * 2))
            resized_frame = cv2.resize(img, (int(frame_width * scaling_factor), int(frame_height * scaling_factor)))

            cv2.imshow('vdo', resized_frame)
            k=cv2.waitKey(1)
            if k==ord('q'):
                break  
        else:
            break
    vdo.release()
    cv2.destroyAllWindows()



def video_screen(): 
    frm=Frame(win, bg='sky blue')
    frm.place(relx=0, rely=.15, relwidth=1, relheight=1)
  
    btn_Browse=Button(frm, command=lambda: browse_video(), text="Browse", font=('',20,'bold'), bd=10, width=8)
    btn_Browse.place(relx=.37, rely=.05)
    btn_back=Button(frm, command=lambda: welcome_screen(), text="back", font=('',20,'bold'), bd=10)
    btn_back.place(relx=.9, rely=0)


    
    
    
    

#----------------------------------------xxxxxxxxxxxxxxxxxxxxxxxxxxxx-----------------------------------------------   
    
   




    
    
    
#--------------------------------------------WebCam-----------------------------------------------------------------
flag=True  
clf=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def stop():
    cap.release()
    lmain.destroy()
    imageFrame.destroy()

def startfac():
    global flag
    flag=True

def stopface():
    global flag
    flag=False

def show_frame():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
    faces=clf.detectMultiScale(gray,1.3,7)
    for x,y,w,h in faces:
        if(flag==True):
            cv2.rectangle(cv2image,(x,y),(x+w,y+h),(255,0,0),2)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame) #calls show_frame after 10 mills

def start():
    global lmain,cap,lmain,imageFrame
    cap=cv2.VideoCapture(0)
    imageFrame=Frame(width=1500,height=2000,bd=1,bg='green')
    lmain=Label(imageFrame)
    lmain.grid(row=5, column=10)
    imageFrame.place(relx=.3,rely=.3)
    btn_DetectFace=Button(imageFrame,command=lambda:startfac(),text='detect face',font=('',20,'bold'),bd=10,width=12).place(relx=.1,rely=.8)
    btn_Stop=Button(imageFrame,command=lambda:stopface(),text='stop detecting',font=('',20,'bold'),bd=10,width=12).place(relx=.5,rely=.9)
    
    show_frame()
    
def webcam_screen():
    frm=Frame(win,bg='sky blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    btn_StartCam=Button(command=lambda:start(),text='start camera ',font=('',20,'bold'),bd=10).place(relx=.01,rely=.2)
    btn_StopCam=Button(command=lambda:stop(),text='stop camera',font=('',20,'bold'),bd=10).place(relx=.01,rely=.4)
    btn_back=Button(frm,command=lambda:welcome_screen(),text="back",font=('',20,'bold'),bd=10)
    btn_back.place(relx=.9,rely=0)
    
#-------------------------------------------------xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx------------------------------------------


def logout():
    option=messagebox.askyesno('Confirmation','Do you want to logout?')
    if(option==True):
        home_screen()
    else:
        pass


def home_screen():
    frm=Frame(win,bg='sky blue')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=1)
    
    lbl_user=Label(frm,text="Username",font=('',20,'bold'),bg='sky blue')
    lbl_user.place(relx=.3,rely=.3)

    entry_user=Entry(frm,font=('',20,'bold'),bd=10)
    entry_user.place(relx=.42,rely=.3)
    entry_user.focus()

    lbl_pass=Label(frm,text="Password",font=('',20,'bold'),bg='sky blue')
    lbl_pass.place(relx=.3,rely=.4)

    entry_pass=Entry(frm,font=('',20,'bold'),bd=10,show="*")
    entry_pass.place(relx=.42,rely=.4)

    btn_login=Button(frm,command=lambda:welcome_screen(entry_user,entry_pass),text="login",font=('',20,'bold'),bd=10,width=10)
    btn_login.place(relx=.45,rely=.5)
        
    
def welcome_screen(entry_user=None,entry_pass=None):
    if(entry_user!=None and entry_pass!=None):
        user=entry_user.get()
        pwd=entry_pass.get()
    else:
        user="admin"
        pwd="admin"
    if(len(user)==0 or len(pwd)==0):
        messagebox.showwarning("validation","Please fill both fields")
        return
    else:
        if(user=="admin" or pwd=="admin"):
            frm=Frame(win,bg='skyblue')
            frm.place(relx=0,rely=.15,relwidth=1,relheight=1)

            btn_image=Button(frm,command=lambda:image_screen(),text="Use Image",font=('',20,'bold'),bd=10,width=25)
            btn_image.place(relx=.35,rely=.2)

            btn_video=Button(frm,command=lambda:video_screen(),text="Use Video",font=('',20,'bold'),bd=10,width=25)
            btn_video.place(relx=.35,rely=.4)
            
            btn_webcam=Button(frm,command=lambda:webcam_screen(),text="Use Webcam",font=('',20,'bold'),bd=10,width=25)
            btn_webcam.place(relx=.35,rely=.6)

            btn_logout=Button(frm,command=lambda:logout(),text="logout",font=('',20,'bold'),bd=10)
            btn_logout.place(relx=.9,rely=0)
        else:
            messagebox.showerror("Fail","Invalid Username/Password")    
    
    
home_screen()
win.mainloop()
