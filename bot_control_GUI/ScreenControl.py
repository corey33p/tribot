from tkinter import *
from tkinter import Canvas,mainloop,Toplevel,Label,Entry,Button
from PIL import Image, ImageTk
import cv2

class ScreenControl:
    def __init__(self,width=800,height=640):
        self.width = width
        self.height = height
        self.setup_window()
        self.show_frames()
        mainloop()
    def setup_window(self):
        self.win = Tk()
        geometry_string = str(self.width)+"x"+str(self.height)
        self.win.geometry(geometry_string)
        self.canvas =Canvas(self.win,width=self.width,height=self.height)
        self.canvas.pack()
        self.cap= cv2.VideoCapture(0)
        
        # setup to capture Canvas click events
        self.canvas.bind("<Button-1>",self.click_function)
        
        # load settings thumbnail
        self.thumbnail_size = int(min(self.width,self.height)/10)
        pil_img = Image.open('source/settings_icon.gif').resize((self.thumbnail_size,self.thumbnail_size), Image.ANTIALIAS)
        self.settings_im=ImageTk.PhotoImage(pil_img)
    def show_frames(self):
        cv2image= cv2.cvtColor(self.cap.read()[1],cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image = frame)
        self.canvas.create_image(0,0,anchor=NW,image=imgtk)
        self.canvas.create_image(0,0,anchor=NW,image=self.settings_im)
        self.canvas.image_ref = imgtk # save the image so it doesn't get destroyed when you leave the scope of the function
        self.canvas.after(20, self.show_frames)
    def click_function(self,event):
        x = event.x
        y = event.y
        if x+y<2*self.thumbnail_size:
            self.config_window()
    def set_button(self,button):
        if button == "forward":
            pass
    def load_controls(self):
        control_config_file = "/config/controls.txt"
        if not os.path.isfile(control_config_file):
            self.controls = {}
            self.controls["<Up>"] = "forward"
        else:
            with open(control_config_file,"r") as f:
                data = f.read()
            lines = data.split("\n")
            for line in lines:
                key,command = line.split(",")
                self.controls[key] = command
    def config_window(self):
        settings_window = Toplevel(self.win)
        
        # forward
        forward_label = Label(settings_window,text="Forward")
        forward_label.grid(row=0,column=0)
        forward_entry = Entry(settings_window,justify='center',width=14)
        forward_entry.grid(row=0,column=1)
        forward_set_button = Button(settings_window,
                                    command=lambda: self.set_button("forward"),
                                    text="Set",
                                    width=3)
        forward_set_button.grid(row=0,column=2)
        
        # done button
        done_button = Button(settings_window,
                             command=settings_window.destroy,
                             text="Done",
                             width=4)
        done_button.grid(row=10,column=0,columnspan=3,sticky="ew")
if __name__ == '__main__':
    sc = ScreenControl()
