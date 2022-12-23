from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


def browse_images():
    global img

    file_name = filedialog.askopenfilename(initialdir='D:/Photo/Foto Diri',
                                           title="Select Image",
                                           )
    img = Image.open(file_name)

    while img.width > right_frame['width'] or img.height > right_frame['height']:
        img = img.resize((int(img.width / 2), int(img.height / 2)))

    tk_image = ImageTk.PhotoImage(img)
    image_label.configure(image=tk_image)
    image_label.image = tk_image


def add_water_mark():
    global img
    if img is not None:
        temp_img = img.copy()
        wm_text = edit_text_en.get()
        selected_font = edit_font_combo.get()
        a_font = a_font = ImageFont.truetype(font='arial.ttf', size=25)
        if selected_font == "Arial":
            a_font = ImageFont.truetype(font='arial.ttf', size=25)
        elif selected_font == "Montserrat-Black":
            a_font = ImageFont.truetype("fonts/Montserrat/static/Montserrat-Black.ttf", size=25)
        elif selected_font == "EagleLake-Regular":
            a_font = ImageFont.truetype("fonts/Eagle_Lake/EagleLake-Regular.ttf", size=25)
        elif selected_font == "TradeWinds-Regular":
            a_font = ImageFont.truetype("fonts/Trade_Winds/TradeWinds-Regular.ttf", size=25)
        img_draw = ImageDraw.Draw(temp_img)
        img_draw.text((int(temp_img.width / 2), int(temp_img.height / 2)), text=wm_text, font=a_font,
                      fill='#FFF', stroke_width=5, stroke_fill='#222', anchor='ms')
        tk_image = ImageTk.PhotoImage(temp_img)
        image_label.configure(image=tk_image)
        image_label.image = tk_image
    else:
        messagebox.showerror("No Image", "Upload an image first.")


window = Tk()

img = None

left_frame = Frame(window, width=200, height=600, padx=5, pady=5)
left_frame.grid(column=0, row=0, sticky=N)

lb_config = Label(left_frame, text="Edit Tools", bg=left_frame["bg"])
lb_config.grid(column=0, row=0)

upload_button = Button(left_frame, text="Upload", command=browse_images)
upload_button.grid(column=0, row=1, sticky=EW)

add_wm_button = Button(left_frame, text="Add Watermark", command=add_water_mark)
add_wm_button.grid(column=0, row=2, sticky=EW)

edit_frame = Frame(left_frame, bg="white")
edit_frame.grid(column=0, row=3)

edit_text_lb = Label(edit_frame, text="Text")
edit_text_en = Entry(edit_frame)
edit_text_en.insert(0, "Text")
edit_text_lb.grid(column=0, row=0, sticky=EW)
edit_text_en.grid(column=1, row=0, sticky=EW)

font_list = ["Arial", "Montserrat-Black", "EagleLake-Regular", "TradeWinds-Regular"]
edit_font_lb = Label(edit_frame, text='Font')
edit_font_combo = Combobox(edit_frame, values=font_list)
edit_font_lb.grid(column=0, row=1, sticky=EW)
edit_font_combo.grid(column=1, row=1, sticky=EW)

edit_color_lb = Label(edit_frame, text='Color')
edit_color_en = Entry(edit_frame)
edit_color_lb.grid(column=0, row=2, sticky=EW)
edit_color_en.grid(column=1, row=2, sticky=EW)

edit_size_lb = Label(edit_frame, text='Size')
edit_size_en = Entry(edit_frame)
edit_size_lb.grid(column=0, row=3, sticky=EW)
edit_size_en.grid(column=1, row=3, sticky=EW)

opacity_lb = Label(edit_frame, text="Opacity")
opacity_scale = Scale(edit_frame, from_=0, to=100, orient=HORIZONTAL)
opacity_lb.grid(column=0, row=4, sticky=EW)
opacity_scale.grid(column=1, row=4, sticky=EW)

rotation_lb = Label(edit_frame, text="Rotation")
rotation_scale = Scale(edit_frame, from_=0, to=100, orient=HORIZONTAL)
rotation_lb.grid(column=0, row=5, sticky=EW)
rotation_scale.grid(column=1, row=5, sticky=EW)

remove_btn = Button(edit_frame, text="Remove Watermark")
remove_btn.grid(column=0, row=6, sticky=EW)

save_btn = Button(edit_frame, text="Save Image")
save_btn.grid(column=1, row=6, sticky=EW)


right_frame = Frame(window, width=800, height=800, padx=5, pady=5)
right_frame.grid(column=1, row=0)

image_label = Label(right_frame, width=800, height=600, text="No Photo")
image_label.grid(column=0, row=0)

window.mainloop()
