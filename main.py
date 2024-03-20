from tkinter import *
from PIL import ImageTk, Image, ImageGrab
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class ImageWatermarking(Tk):
    def __init__(self):
        super().__init__()
        self.fonts = ["Arial","Times","Helvetica","Impact","Georgia"]
        self.font_sizes = [12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42]
        self.colors = ["blue","red","green","lightblue","purple","pink"]
        self.c_texts = []
        self.create_canvas()
        self.create_menu()
        self.canvas.bind("<B1-Motion>",func=self.change_position)
        self.canvas.bind("<B3-Motion>",func=self.change_logo_position)
        
    def create_canvas(self):
        self.title("Image Watermarking App")
        self.geometry("1000x800")
        self.canvas = Canvas(master=self, width=1000, height=800)
        self.canvas.pack()
        self.photo_image = None


    def create_menu(self):
        menu_bar = Menu(master=self)
        self.config(menu=menu_bar)
        menu_bar.add_command(
            label="Add Photo",
            command=self.add_photo
        )
        menu_bar.add_command(
            label="Resize Image",
            command=self.top_level
        )
        menu_bar.add_command(
            label="Add Text",
            command=self.top_level_2
        )
        menu_bar.add_command(
            label="Delete Text",
            command=self.delete_text
        )
        menu_bar.add_command(
            label="Add Logo",
            command=self.add_logo
        )
        menu_bar.add_command(
        label="Save Photo",
        command=self.take_screenshot
    )
        menu_bar.add_command(label="Exit", command=quit)
       

    def add_photo(self):
        self.file_path = fd.askopenfilename()
        if self.file_path:
            img = Image.open(self.file_path)
            width, height = img.size

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if width > canvas_width or height > canvas_height:
                ratio = min(canvas_width/width,canvas_height/height)
                width = int(width*ratio)
                height = int(height*ratio)
                img = img.resize((width,height),Image.LANCZOS)

            x = (canvas_width - width) // 2
            y = (canvas_height - height) // 2
            self.photo_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(x, y, anchor=NW, image=self.photo_image)

    def top_level(self):
        top_level = Toplevel(master=self)
        top_level.geometry("200x200")
        top_level.title("Resize Image")
        Label(master=top_level,text="Enter your width").pack()
        self.new_width = Entry(master=top_level)
        self.new_width.pack()
        Label(master=top_level,text="Enter your height").pack()
        self.new_height = Entry(master=top_level)
        self.new_height.pack()
        Button(master=top_level,text="Done",command=self.resize_img).pack()

    def resize_img(self):
        try:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if self.new_width or self.new_height:
                img = Image.open(self.file_path)
                width,height = int(self.new_width.get()),int(self.new_height.get())
                img = img.resize((width,height),Image.LANCZOS)
                self.photo_image = ImageTk.PhotoImage(img)
                x = (canvas_width - width) // 2
                y = (canvas_height - height) // 2
                self.canvas.create_image(x,y,anchor=NW,image=self.photo_image)
        except Exception:
            mb.showerror("Error","Something went wrong or wrong value, please try again")
            print(Exception)
    
    def top_level_2(self):
        top_level2 = Toplevel(master=self)
        top_level2.title("Properties")
        Label(master=top_level2,text="Text").grid(row=0,column=0)
        self.text = Entry(master=top_level2,textvariable="Your Text")
        self.text.grid(row=0,column=1)
        Label(master=top_level2,text="Font").grid(row=1,column=0)
        self.value_inside = StringVar(top_level2)
        self.value_inside.set("Select An Option")
        OptionMenu(top_level2,self.value_inside, *self.fonts).grid(row=1,column=1)
        Label(master=top_level2,text="Color").grid(row=2,column=0)
        self.value_inside_2 = StringVar(top_level2)
        self.value_inside_2.set("Select an Option")
        OptionMenu(top_level2,self.value_inside_2, *self.colors).grid(row=2,column=1)
        Label(master=top_level2,text="Font Size").grid(row=3,column=0)
        self.values_inside_3 = StringVar(top_level2)
        self.values_inside_3.set("Select an Option")
        OptionMenu(top_level2,self.values_inside_3, *self.font_sizes).grid(row=3,column=1)
        Button(master=top_level2,text="Add Text",command=self.add_text).grid(row=4,column=0)
    def add_text(self):
        try:
            height = self.photo_image.height()
            width = self.photo_image.width()
            font = f'{self.value_inside.get()} '+f'{int(self.values_inside_3.get())}'
            self.c_text = self.canvas.create_text((width/2,height/2), text=self.text.get(), fill=self.value_inside_2.get(),font=(font))
            self.c_texts.append(self.c_text)
        except:
            mb.showerror("Error","Something went wrong")

    def delete_text(self):
        for c_text in self.c_texts:
            self.canvas.delete(c_text)

    def change_position(self,event):
        x = event.x
        y = event.y
        # 20x20 square around mouse to make sure text only gets targeted if the mouse is near it
        for text in self.c_texts:
            if text in self.canvas.find_overlapping(str(x-10), str(y-10), str(x+10), str(y+10)):
                self.canvas.coords(text, x, y)
    
    def add_logo(self):
        self.logo_path = fd.askopenfilename()
        if self.logo_path:
            img = Image.open(self.logo_path)
            width, height = img.size

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

           
            ratio = min(canvas_width/width,canvas_height/height)
            width = int(width*ratio) // 10
            height = int(height*ratio)  // 10
            img = img.resize((width,height),Image.LANCZOS)

            x = (canvas_width - width) // 2
            y = (canvas_height - height) // 2
        self.logo_image = ImageTk.PhotoImage(img)
        self.logo = self.canvas.create_image(x, y, anchor=NW, image=self.logo_image)

    def change_logo_position(self,event):
        x = event.x
        y = event.y
        self.canvas.coords(self.logo,x,y)    

    def take_screenshot(self):
        if self.photo_image:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()

            # Ekran görüntüsünü alın ve kaydedin
            screenshot = ImageGrab.grab(bbox=(x, y, x+ width, y+height))
            screenshot.save("screenshot.png")
        else:
            mb.showerror("Error", "No image loaded.")



def main():
    img_wm = ImageWatermarking()
    img_wm.mainloop()

if __name__ == "__main__":
    main()