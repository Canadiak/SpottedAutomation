#Files for saving text as images
from PIL import Image, ImageDraw, ImageFont
import textwrap

MAX_W, MAX_H = 520, 520

class ImageMaker:

    def __init__(self):
        pass

    def make_image_from_string(self, text, id_tag, time_stamp):
        img = Image.new('RGB', (MAX_W, MAX_H), (251, 207, 232))
        d = ImageDraw.Draw(img)
        
        fnt = ImageFont.truetype('Noto_Sans_Display\NotoSansDisplay-VariableFont_wdth,wght.ttf', 14)
        current_h, pad = 100, 8 # current_h is the y position for the text line to be put at, pad is the padding
        for line in text:
            h = d.textsize(line, font=fnt)[1] # h is the height of the font
            d.text((30, current_h), line, font=fnt, fill=(0, 0, 0))
            current_h += h + pad

        d.text((30, current_h+30), id_tag, font=fnt, fill=(0, 0, 0))

        
        # Format: Timestamp + __ + img_number
        img_name = time_stamp + "__" + ".jpg"
        img_name = img_name.replace('/', '-')
        img_name = img_name.replace(':', '-')
        folder = "Image_Folder\\"
        path = folder + img_name
        img.save(path)
        return path
        
    def split_up_string(self, text):
        split_string = textwrap.wrap(text, width = 55)
        print(split_string)
        #self.make_image_from_string(split_string)
        return split_string

    def make_image(self, body_text, id_tag, time_stamp):
        body_text = self.split_up_string(body_text)
        return self.make_image_from_string(body_text, id_tag, time_stamp)

        
if __name__ == '__main__':
    test_string = '😀 🤖 Hello'  #"🤖sagittis, dui eros sagittis diam, eu mattis  Nam et metus non turpis facilisis tristique ac vitae mauris. Nam placerat est non ipsum faucibus vestibulum. Suspendisse fermentum nunc egestas dapibus sodales. Pellentesque  diam, eu mattis  Nam et metus non turpis facilisis tristique ac vitae mauris. Nam placerat est non ipsum faucibus vestibulum. Suspendisse fermentum nunc egestas dapibus sodales. Pellentesque fermentum turpis ac lobortis tincidunt. Integer nec rhoncus lacus. Etiam quis sapien enim. Nulla condimentum, sapien sit amet ultrices sagittis, dui eros sagittis diam, eu mattis leo ante id metus. Fusce venenatis eros id eros placerat pretium."
    image_maker = ImageMaker()
    image_maker.split_up_string(test_string)
    image_maker.make_image_from_string(test_string, "test id", "Noto2")