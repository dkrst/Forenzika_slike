from PIL import Image
import piexif

# Otvorimo izvornu sliku
img = Image.open('DSC_2326.JPG')

# Izdvojimo ROI (Region of Interest)
roi=(1400,600,2000,1600)
part = img.crop(roi)

# Zaljepimo ROI na novu lokaciju (copy/paste manipulacija)
img.paste(part, (0, 700, 600, 1700))
img.save('manip.jpg', quality=100)

# Usporedimo EXIF zapise za izvornu i manipuliranu sliku
# U konzoli:
#
'''
exiftool manip.jpg > manip.out
exiftool DSC_2326.JPG > orig.out
diff manip.out orig.out | less   # Krivotvorina vidljiva iz aviona!
'''

# Izdvojimo THUMBNAIL iz JPEG datoteke
exif_orig = piexif.load('DSC_2326.JPG')
orig_tmb_bytes = exif_orig.pop('thumbnail')

with open('tmb_orig.jpg', 'wb+') as f:
    f.write(orig_tmb_bytes)

exif_hide = piexif.load('manip.jpg')
manip_tmb_bytes = exif_hide.pop('thumbnail')

with open('tmb_manip.jpg', 'wb+') as f:
    f.write(manip_tmb_bytes)

# Provjerimo tip podataka za orig_tmb_bytes i manip_tmb_bytes
#
type(orig_tmb_bytes)
type(manip_tmb_bytes)

# Kopiram sliku (datoteku) manip.jpg u hide.jpg
# U konzoli:
#
'''
cp manip.jpg hide.jpg
diff hide.jpg manip.jpg         # Datoteke su identične!
exiftool hide.jpg > hide.out
diff hide.out manip.out | less  # Razlike samo vezane uz datoteku
'''

# Kopirajmo EXIF zapis iz izvorne slike u manipuliranu (hide.jpg)
piexif.transplant('DSC_2326.JPG', 'hide.jpg')

# U konzoli (u direktoriju work):
#
'''
exiftool hide.jpg > hide.out
diff hide.out orig.out | less  # Razlike samo vezane uz datoteku
diff hide.out manip.out | less # Razlike su očite!
'''

exif_hide = piexif.load('hide.jpg')
hide_tmb_bytes = exif_hide.pop('thumbnail')

with open('tmb_hide.jpg', 'wb+') as f:
    f.write(hide_tmb_bytes)

type(hide_tmb_bytes)

# Radim novi thumbnail za hide.jpg
# Prvo kopiram stari da mi ostane
''' U konzoli:
mv tmb_hide.jpg tmb_hide-0.jpg
'''

# Provjerimo dimenzije thumbnaila za izvornu sliku i hide.jpg
tmb_orig = Image.open('tmb_orig.jpg')
tmb_orig.size

img_hide = Image.open('hide.jpg')
img_hide.thumbnail((160, 120))
img_hide.show()

img_hide.save('tmb_hide.jpg')
img_hide.size

# U konzoli sa exiftool ubaciti novi thumbnail.
'''
exiftool "-thumbnailimage<=tmb_hide.jpg" hide.jpg
'''
# Za provjeru: ponovo izdvojimo thumbnail iz hide.jpg
exif_hide = piexif.load('hide.jpg')
hide_tmb_bytes = exif_hide.pop('thumbnail')

with open('tmb_hide-1.jpg', 'wb+') as f:
    f.write(hide_tmb_bytes)

type(hide_tmb_bytes)


# Prikazimo thumbnailove za izvornu i manipuliranu sliku,
# jedan kraj drugog
tmb_hide = Image.open('tmb_hide.jpg')
tmb_hide.size
tw = tmb_hide.width + tmb_orig.width
mh = max(tmb_hide.height, tmb_orig.height)
# Radim thumbnail na pravu velicinu, sa crnim rubom (kao original)
thumbnails = Image.new('RGB', (tw, mh))
thumbnails.paste(tmb_hide, (0, 0))
thumbnails.paste(tmb_orig, (tmb_hide.width, 0))

thumbnails.show()

# Radim thumbnail na pravu velicinu, sa crnim rubom (kao original)
hide_tmb = Image.new('RGB', (160,120), (0,0,0))
tw, th = hide_tmb.size

hide_tmb_roi = Image.open('hide.jpg')
hide_tmb_roi.thumbnail((160, 120))
roiw, roih = hide_tmb_roi.size

ys = int((th-roih)/2)
ye = ys + roih

hide_tmb.paste(hide_tmb_roi, (0, ys, tw, ye))
hide_tmb.save('tmb_hide.jpg')

# U konzoli sa exiftool ubaciti novi thumbnail.
# ponovo usporediti exif zaglavlja sa exiftool i diff

'''
exiftool "-thumbnailimage<=tmb_hide.jpg" hide.jpg
exiftool hide.jpg > hide.out
diff hide.out orig.out | less  # Razlike samo vezane uz datoteku
'''


# Dventualno nastimat kvalitetu thumbnaila da velicina
# datoteke bude slicna kao za originalni thumbnail

