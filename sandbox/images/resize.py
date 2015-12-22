import StringIO
import Image
import argparse
import logging
import os
import scipy
from scipy.optimize._minimize import minimize_scalar
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


def get_ratio_for_file_size(path, target_size):
    if os.path.getsize(path) < target_size:
        return 1.0

    def f(ratio):
        ntf = NamedTemporaryFile(delete=False)
        ntf.write(resize_image(ratio, path))
        ntf.close()
        fsize = os.path.getsize(ntf.name)
        return abs(fsize - target_size)

    r = minimize_scalar(f, method='Bounded', bounds=(0.1, 1.0))
    return r.x


def resize_dir():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='the path to the directory containing the images '
                                    'to be resized. All images contained in the directory '
                                    'will be processed.')
    def _positive_int(val):
        myval = int(val)
        if myval <= 10:
            raise ValueError('too small value provided for target size (must be > 10)')
        return myval

    parser.add_argument('-t', help='target size (in bytes) of the images.',
                        default=None, required=True, type=_positive_int)
    opt = parser.parse_args()
    if not os.path.exists(opt.dir):
        raise Exception('the specified path {} does not exist!'.format(opt.dir))
    for fname in os.listdir(opt.dir):
        try:
            file_path = os.path.join(opt.dir, fname)
            best_ratio = get_ratio_for_file_size(file_path, opt.t)
            if best_ratio >= 1.0:
                raise Exception('could not minimize {}'.format(file_path))
            new_file_path = os.path.join(opt.dir, 'new_{}'.format(fname))
            if os.path.exists(new_file_path):
                raise Exception('file {} exist already'.format(new_file_path))
            with open(new_file_path, 'w') as f:
                f.write(resize_image(best_ratio, file_path))
            logging.info('image {} resized to {}, ratio {}'.format(file_path,
                                                                   new_file_path,
                                                                   best_ratio))
        except Exception as e:
            logging.exception(e)


if __name__ == '__main__':
    resize_dir()

