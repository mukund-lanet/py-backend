from pdf2image import convert_from_path
import time

start = time.time()
images = convert_from_path(input('ENter the pdf URL: '))

for i in range(len(images)):
    # Save pages as images in the pdf
    images[i].save('images/page'+ str(i) +'.jpg', 'JPEG')

end = time.time()
print(end - start)