from os import listdir
from os.path import isfile,join,getsize
from PIL import Image


from django.core.files import File
from io import BytesIO
from PIL import Image,ImageFile

def compress_image(image,path):
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    print(path)
    #im.save(im_io, 'jpeg', quality=40,optimize=True)
    



mypath = 'media/img/products/22'



onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
im_io = BytesIO()
normal_size = 0.3*1024*1024
print (normal_size)
ImageFile.LOAD_TRUNCATED_IMAGES = True
for imagename in onlyfiles:
    path = mypath+'/'+imagename 
    img_size = getsize(path)
    quality = 35
   
    if img_size >= normal_size:
            print(str(img_size) +': ' +imagename)
            img = Image.open(mypath+'/'+imagename)
            if img:
                if not img.mode =='RGB':
                    img = img.convert('RGB')
                print(quality,'  Image Size:', img_size )
                img.save(path,quality=quality,optimize=True)
                print('Converted')
    
    

         

print('Finsished...')