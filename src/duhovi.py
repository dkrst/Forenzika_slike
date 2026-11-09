from PIL import Image            # Python Image Library
from PIL import ImageChops       # Image Channel Operations
from os import listdir           # Vise-manje potrebno
import matplotlib.pyplot as plt  # pyplot - prikaz
import numpy as np               # numpy matematicki lib

listdir('.')
img=Image.open('DSC_2326.JPG')   # Ucitavanje proizvoljne slike
img.show()                       # prikaz slike

img.save('img60.jpg', quality=60)  # snimanje s kvalitetom 60
img.save('img90.jpg', quality=90)  # snimanje s kvalitetom 90

roi=(1400,600,2000,1600)

part=img.crop(roi)
part.show()

im60=Image.open('img60.jpg')
im90=Image.open('img90.jpg')

part60=im60.crop(roi)

# Paste na "krivo" misto
img_manip=im90.copy()
img_manip.paste(part60, (0,700,600,1700))
img_manip.show()

# Paste na pravo misto
img_manip=im90.copy()
img_manip.paste(part60, roi)
img_manip.show()

img_manip.save('manip90.jpg', quality=90)

img_test=Image.open('manip90.jpg')

img_test.show()

# Za jednu razinu kompresije
img_test.save('tmp060.jpg', quality=60)
img_tmp = Image.open('tmp060.jpg')
img_diff = ImageChops.difference(img_test, img_tmp)

img_diff.show()

# Definirajmo funkciju za normalizaciju na range [0,255]
# (istice male razlike)
def normalize(arr):
    arr2 = arr.astype('float')
    for i in range(3):
        minval = arr2[...,i].min()
        maxval = arr2[...,i].max()
        if minval != maxval:
            arr2[...,i] -= minval
            arr2[...,i] *= (255.0/(maxval-minval))
    return arr2

a_diff = np.array(img_diff)
a_diff.shape

out_img = Image.fromarray(normalize(a_diff).astype('uint8'), 'RGB')
out_img.show()

# Dodatno istaknimo razlike u sliku sivih razina
# i normalizirajmo rezultirajucu sliku razlike
c0 = a_diff[..., 0]
c1 = a_diff[..., 1]
c2 = a_diff[..., 2]

cs = c0**2 + c1**2 + c2**2
gl_diff = Image.fromarray(normalize(cs).astype('uint8'))
gl_diff.show()

# OK, sada smo znali da je na slici kvalitete 90 ubacen
# dio komprimiran sa kvalitetom 60
# Napisimo funkciju koja provjerava za razne razine
# kvalitete
qrng =  [x for x in range(20,101, 10)]
nq = len(qrng)

# Za pregled po raznim razinama kompresije
for q in qrng:
    # spremam sliku sa zadanom raznim kompresije
    img_test.save('tmp%03d.jpg'%q, quality=q)
    #ucitavam spremljenu sliku
    img_tmp = Image.open('tmp%03d.jpg'%q)
    #racunam razliku
    img_diff = ImageChops.difference(img_test, img_tmp)
    # pretvaram u numpy array i razvajam na 3 kanalaRGB kanale
    a_diff = np.array(img_diff)
    c0 = a_diff[..., 0]
    c1 = a_diff[..., 1]
    c2 = a_diff[..., 2]
    # kompozitna GL slika - pojacavam kvadriranjem
    cs = c0**2 + c1**2 + c2**2
    #normalizacija
    gl_diff = Image.fromarray(normalize(cs).astype('uint8'))
    #prikaz
    gl_diff.show()
   
# Prikaz sumarno na manjoj slici po blokovima

ah, aw = cs.shape

bs = 8
bh = int((ah-bs)/bs)
bw = int((aw-bs)/bs)

blk_diff = np.zeros((bh,bw))
for ys in range(bh):
    for xs in range (bw):
        blk_diff[ys, xs] = np.mean(cs[ys*bs:(ys+1)*bs, xs*bs:(xs+1)*bs])

blk_img = Image.fromarray(normalize(blk_diff).astype('uint8'))


# Prikaz po blokovima za razne razine kompresije

qrng =  [x for x in range(20,101, 10)]
nq = len(qrng)

imgw, imgh = img_test.size
bs = 8
bh = int((imgh-bs)/bs)
bw = int((imgw-bs)/bs)

blk_all = np.zeros((bh, bw, nq))  # moze se dodat i posli :-)
blk_img = []

cnt = 0 # ovo ne triba ako se dodaje posli, triba dodat posli :-)

for q in qrng:
    # spremam sliku sa zadanom raznim kompresije
    img_test.save('tmp%03d.jpg'%q, quality=q)
    #ucitavam spremljenu sliku
    img_tmp = Image.open('tmp%03d.jpg'%q)
    #racunam razliku
    img_diff = ImageChops.difference(img_test, img_tmp)
    # pretvaram u numpy array i razvajam na 3 kanalaRGB kanale
    a_diff = np.array(img_diff)
    c0 = a_diff[..., 0]
    c1 = a_diff[..., 1]
    c2 = a_diff[..., 2]
    # kompozitna GL slika - pojacavam kvadriranjem
    cs = c0**2 + c1**2 + c2**2
    # U petlji prolazim kroz sliku korakom sirine bloka i racunam mean
    blk_diff = np.zeros((bh, bw))
    for ys in range(bh):
        for xs in range (bw):
            blk_diff[ys, xs] = np.mean(cs[ys*bs:(ys+1)*bs, xs*bs:(xs+1)*bs])
    # dodajem u listu slika sliku novog bloka
    blk_img.append(Image.fromarray(normalize(blk_diff).astype('uint8')))
    blk_all[...,cnt] = np.copy(blk_diff)
    cnt += 1

# prikaz jedne od blokovskih slika razlike
blk_img[0].show()

# Prikaz u multiplotu
for cnt in range (nq):
    plt.subplot(3, 3, cnt+1)
    plt.imshow(blk_all[...,cnt])
    plt.axis('off')
    plt.title('ql: %3d'%qrng[cnt])

plt.show()
    
