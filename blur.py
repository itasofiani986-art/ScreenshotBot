from PIL import Image, ImageFilter
import os



def blur_area(img, x, y, w, h):

    area = img.crop(
        (
            x,
            y,
            x+w,
            y+h
        )
    )


    area = area.filter(
        ImageFilter.GaussianBlur(10)
    )


    img.paste(
        area,
        (
            x,
            y
        )
    )





def blur_image_text(image_path, boxes=None):


    if not os.path.exists(image_path):

        print("FILE TIDAK ADA")
        return



    img = Image.open(image_path).convert("RGB")


    print("================")
    print("BLUR MULAI")
    print(img.size)
    print("================")



    if not boxes:

        print("TIDAK ADA BOX SENSOR")

        img.save(image_path)

        return




    for b in boxes:


        print(
            "BLUR BOX",
            b
        )


        blur_area(

            img,

            int(b["x"]),

            int(b["y"]),

            int(b["width"]),

            int(b["height"])

        )




    img.save(image_path)


    print("BLUR SELESAI")