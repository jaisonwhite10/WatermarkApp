from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageDraw,ImageFont

window = Tk()
canvas = Canvas(width=1000,height=1000)
canvas.grid(column=3,row=3)
def upload():

    global image
    global original_image_width
    global original_image_height

    filename = filedialog.askopenfilename(title='Select an Image')
    image = Image.open(filename)
    original_image_width = image.width
    original_image_height = image.height

    res_img = image.resize((600,600))
    new_image = ImageTk.PhotoImage(res_img)
    photo = Label(image=new_image)
    photo.image = new_image
    # photo.grid(column=0,row=0)
    photo.place(x=0, y=0)



def watermark():

    global image
    global copied_image
    global resized_copied_image
    global cop_res_img
    global final_composite

    image_width = image.width

    copied_image = image.copy()
    resized_copied_image = copied_image.resize((600, 600)).convert('RGBA')
    cop_res_img = Image.new('RGBA', resized_copied_image.size, (255, 255, 255, 0))#.rotate(angle=180)

    ##watermark_image
    rotated_res_img = Image.new('RGBA', resized_copied_image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(cop_res_img)

    font_size = int(watermark_font_entry.get())
    font = ImageFont.truetype('arial.ttf', font_size)

    x = int(watermark_x_entry.get())
    y = int(watermark_y_entry.get())
    draw.text((x, y), text=watermark_entry.get(), font=font, fill=(255,255,255,watermark_opacity_scale.get()), anchor='ms')

    rotated_text_image = cop_res_img.rotate(angle=int(rotate_watermark_entry.get()),expand=True,fillcolor=(0,0,0,0))
    rotated_text_image_size = rotated_text_image.size

    rotated_x = resized_copied_image.size[0] // 2 - rotated_text_image_size[0] // 2
    rotated_y = resized_copied_image.size[1] // 2 - rotated_text_image_size[1] // 2

    rotated_res_img.paste(rotated_text_image,(rotated_x,rotated_y))
    composite = Image.alpha_composite(resized_copied_image, cop_res_img)
    final_composite = Image.alpha_composite(resized_copied_image, rotated_res_img)

    new_image = ImageTk.PhotoImage(composite)
    new_image_rotated_watermark = ImageTk.PhotoImage(final_composite)

    photo = Label(image=new_image_rotated_watermark)
    photo.image = new_image_rotated_watermark

    photo.place(x=0, y=0)


def save_photo():

    global final_composite

    final_composite = final_composite.convert('RGB')
    myFormats = [('JPEG', '*.jpg')]
    files = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif'))
    filename = filedialog.asksaveasfile(mode='w',filetypes=files,defaultextension=files)
    if filename:
        final_composite.save(filename)




#instructions
instructions = Label(window,text='Instructions:')
instructions.place(x=545,y=10)
instruction_1 = Label(window,text='1. Please not that the pic uploaded will be placed on coordinates (0,0)')
instruction_1.place(x=545,y=30)

instruction_2 = Label(window,text='2. Adjust the x and y coordinates of the watermark until final product is too your liking.\n(hint: coordinates (400,400) will place mark on bottom right corner of photo')
instruction_2.place(x=543,y=50)

instruction_3 = Label(window,text='3. Please note leaving opacity at 0 will leave watermark blank')
instruction_3.place(x=545,y=90)

instruction_4 = Label(window,text='4. Rotate angle cannot be left blank please enter 0 if you wish to not rotate watermark')
instruction_4.place(x=545,y=130)

upload_button = Button(text='Upload Photo',command=upload,width=12)
upload_button.place(x=900,y=180)
#
watermark_label = Label(window,text='Enter Watermark Here:')
watermark_label.place(x=650,y=230)

watermark_entry = Entry(window,width=35)
watermark_entry.place(x=777,y=230)

watermark_font_label = Label(window,text='Enter watermark font size')
watermark_font_label.place(x=650,y=260)

watermark_font_entry = Entry(window,width=20)
watermark_font_entry.place(x=870,y=260)

watermark_x_label = Label(window,text='Enter Watermark X Coordinate:')
watermark_x_label.place(x=650,y=290)

watermark_x_entry = Entry(window,width=20)
watermark_x_entry.place(x=870,y=290)

watermark_y_label = Label(window,text='Enter Watermark Y Coordinate:')
watermark_y_label.place(x=650,y=320)

watermark_y_entry = Entry(window,width=20)
watermark_y_entry.place(x=870,y=320)

watermark_opacity_label = Label(window,text='Adjust Watermark Opacity:')
watermark_opacity_label.place(x=650,y=360)

watermark_opacity_scale = Scale(window, orient=HORIZONTAL, from_=0,to=255)
watermark_opacity_scale.place(x=900,y=350)

rotate_watermark_label = Label(window,text='Rotate Watermark Angle:')
rotate_watermark_label.place(x=650,y=410)

rotate_watermark_entry = Entry(window,width=20)
rotate_watermark_entry.place(x=870,y=410)

watermark_button = Button(text='Add Watermark',command=watermark)
# watermark_button.grid(row=1,column=1)
watermark_button.place(x=900,y=440)

save_button = Button(text='Save photo',command=save_photo,width=12)
# save_button.grid(row=2,column=1)
save_button.place(x=900,y=500)


window.mainloop()