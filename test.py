from PIL import Image
import numpy as np

from Dermabrasion.imageProcess import beeps


imagepath='./pics/girl0.png'


image=Image.open(imagepath)
image.show()

imgary=np.array(image)

iaf=beeps(imgary,0.08,0.1)

derbra=Image.fromarray(iaf)

derbra.show()