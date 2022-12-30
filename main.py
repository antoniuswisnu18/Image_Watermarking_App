import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.img = None
        self.temp_img = None
        self.color = ((225, 225, 225), '#FFF')
        self.wm_img = None

        self.left_frame = Frame(self, width=200, height=600, padx=5, pady=5)
        self.left_frame.grid(column=0, row=0, sticky=N)

        self.lb_config = Label(self.left_frame, text="Edit Tools", bg=self.left_frame["bg"])
        self.lb_config.grid(column=0, row=0)

        self.upload_button = Button(self.left_frame, text="Upload", command=self.browse_images)
        self.upload_button.grid(column=0, row=1, sticky=EW)

        self.add_wm_button = Button(self.left_frame, text="Add Watermark", command=self.add_watermark)
        self.add_wm_button.grid(column=0, row=2, sticky=EW)

        self.edit_frame = Frame(self.left_frame, bg="white")
        self.edit_frame.grid(column=0, row=3)

        self.edit_text_lb = Label(self.edit_frame, text="Text")
        self.var = StringVar()
        self.var.trace("w", self.add_watermark)
        self.edit_text_en = Entry(self.edit_frame, textvariable=self.var)
        self.edit_text_en.insert(0, "Text")
        self.edit_text_lb.grid(column=0, row=0, sticky=EW)
        self.edit_text_en.grid(column=1, row=0, sticky=EW)

        self.font_list = ["Arial", "Montserrat-Black", "EagleLake-Regular", "TradeWinds-Regular"]
        self.edit_font_lb = Label(self.edit_frame, text='Font')
        self.edit_font_combo = Combobox(self.edit_frame, values=self.font_list)
        self.edit_font_lb.grid(column=0, row=1, sticky=EW)
        self.edit_font_combo.grid(column=1, row=1, sticky=EW)

        self.edit_color_lb = Label(self.edit_frame, text='Color')
        self.edit_color_btn = Button(self.edit_frame, command=self.select_color)
        self.edit_color_lb.grid(column=0, row=2, sticky=EW)
        self.edit_color_btn.grid(column=1, row=2, sticky=EW)

        self.edit_size_lb = Label(self.edit_frame, text='Size')
        self.var_size = IntVar()
        self.var_size.trace("w", self.add_watermark)
        self.edit_size_spinbox = Spinbox(self.edit_frame, from_=10, to=200, textvariable=self.var_size)
        self.edit_size_lb.grid(column=0, row=3, sticky=EW)
        self.edit_size_spinbox.grid(column=1, row=3, sticky=EW)

        self.opacity_lb = Label(self.edit_frame, text="Opacity")
        self.var_opacity = IntVar()
        self.var_opacity.trace('w', self.add_watermark)
        self.opacity_spinbox = Spinbox(self.edit_frame, from_=128, to=225, textvariable=self.var_opacity)
        self.opacity_lb.grid(column=0, row=4, sticky=EW)
        self.opacity_spinbox.grid(column=1, row=4, sticky=EW)

        self.rotation_lb = Label(self.edit_frame, text="Rotation")
        self.rotation_scale = Scale(self.edit_frame, from_=0, to=100, orient=HORIZONTAL)
        self.rotation_lb.grid(column=0, row=5, sticky=EW)
        self.rotation_scale.grid(column=1, row=5, sticky=EW)

        self.remove_btn = Button(self.edit_frame, text="Remove Watermark")
        self.remove_btn.grid(column=0, row=6, sticky=EW)

        self.save_btn = Button(self.edit_frame, text="Save Image")
        self.save_btn.grid(column=1, row=6, sticky=EW)

        self.right_frame = Frame(self, width=800, height=800, padx=5, pady=5)
        self.right_frame.grid(column=1, row=0)

        self.image_label = Label(self.right_frame, width=800, height=600, text="No Photo")
        self.image_label.grid(column=0, row=0)

    def add_watermark(self, *args):
        wm_text = self.var.get()
        selected_font = self.edit_font_combo.get()
        size = int(self.var_size.get())
        opacity = int(self.var_opacity.get())
        color_tuple = self.color[0] + (opacity,)
        print(color_tuple)

        self.temp_img = self.wm_img.copy()
        img_draw = ImageDraw.Draw(self.temp_img)

        if selected_font == "Arial":
            a_font = ImageFont.truetype(font='arial.ttf', size=size)
        elif selected_font == "Montserrat-Black":
            a_font = ImageFont.truetype("fonts/Montserrat/static/Montserrat-Black.ttf", size=size)
        elif selected_font == "EagleLake-Regular":
            a_font = ImageFont.truetype("fonts/Eagle_Lake/EagleLake-Regular.ttf", size=size)
        elif selected_font == "TradeWinds-Regular":
            a_font = ImageFont.truetype("fonts/Trade_Winds/TradeWinds-Regular.ttf", size=size)
        elif selected_font == "":
            a_font = ImageFont.truetype(font='arial.ttf', size=size)

        img_draw.text((int(self.wm_img.width / 2), int(self.wm_img.height / 2)), text=wm_text, font=a_font,
                      fill=color_tuple, stroke_width=5, stroke_fill='#222', anchor='ms')

        combined_img = Image.alpha_composite(self.img, self.temp_img)
        tk_image = ImageTk.PhotoImage(combined_img)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def select_color(self, *args):
        self.color = colorchooser.askcolor(title="Choose Color")
        print(self.color)
        self.edit_color_btn.config(bg=self.color[1])
        self.add_watermark()

    def browse_images(self, *args):
        file_name = filedialog.askopenfilename(initialdir='D:/Photo/Foto Diri',
                                               title="Select Image",
                                               )
        self.img = Image.open(file_name).convert('RGBA')

        while self.img.width > self.right_frame['width'] or self.img.height > self.right_frame['height']:
            self.img = self.img.resize((int(self.img.width / 2), int(self.img.height / 2)))

        self.wm_img = Image.new('RGBA', self.img.size, (225, 225, 225, 0))
        tk_image = ImageTk.PhotoImage(self.img)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image


if __name__ == "__main__":
    app = App()
    app.mainloop()
