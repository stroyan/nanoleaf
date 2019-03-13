
import PIL.ImageGrab

im = PIL.ImageGrab.grab() 
print(im)
im.thumbnail([5,2])
print(im)
px = im.load()
for y in range(2):
  for x in range(5):
    print(px[x,y], end='\t')
  print()
im.show() 
