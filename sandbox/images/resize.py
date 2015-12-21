import StringIO
import Image
import os
from tempfile import NamedTemporaryFile


def resize_image(ratio, path, image_format=None):
    if image_format is None:
        filename, file_extension = os.path.splitext(path)
        image_format = file_extension.strip('.')
    im = Image.open(path)
    old_size = im.size
    im.thumbnail((int(old_size[0]*ratio),
                  int(old_size[1]*ratio)),
                 Image.ANTIALIAS)
    out = StringIO.StringIO()
    im.save(out, image_format)
    val = out.getvalue()
    out.close()
    return val


def resize_to_file_size(path, target_size):
    def f(ratio):
        ntf = NamedTemporaryFile(delete=False)
        ntf.write(resize_image(ratio, path))
        ntf.close()
        fsize = os.path.getsize(ntf.name)
        return abs(fsize - target_size)


if __name__ == '__main__':
    datapath = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(datapath, 'test_resize.jpeg'), 'w') as f:
        f.write(resize_image(0.6, os.path.join(datapath, 'images.jpeg')))
    resize_to_file_size(os.path.join(datapath, 'test_resize.jpeg'), 1000000)


