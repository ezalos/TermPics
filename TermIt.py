from PIL import Image
import cv2
import os

gray_scale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-2]
#gray_scale = " "
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--size", help="Screen size. Usage: --size height width", type=int, nargs=2)
parser.add_argument("-a", "--ascii", help="Display ascii", default=False, action='store_true')
parser.add_argument("-w", "--white", help="Text will have default color", default=False, action='store_true')
args = parser.parse_args()

def conv_to_char(px):
    mean = px
    if len(px) > 1:
        mean = px.mean()
        if args.white == False:
            if args.ascii == True:
                bg = 38
            else:
                bg= 48
            ret = "\x1b[{};2;{};{};{}m".format(bg, px[2], px[1], px[0])
    if args.ascii == True:
        ratio = mean / 255
        ratio = int(ratio * len(gray_scale))
        ret += gray_scale[ratio]
    else:
        ret += " "
    return ret

class TermIt:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        if args.size == None:
            self.rows = int(rows) * 90 // 100
            self.cols = int(cols) * 80 // 100
        else:
            self.rows = args.size[0]
            self.cols = args.size[1]

    def print_it(self, im):
        height = len(im)
        width = len(im[0])
        line = "\033[0;0H"
        w_ratio = int(width / self.cols)
        h_ratio = int(height / self.rows)
        w_ratio = int(w_ratio + (w_ratio * 0.1))
        h_ratio = int(h_ratio + (h_ratio * 0.1))
        p_vert = 0
        while p_vert < height:
            p_horz = 0
            while p_horz < width:
                line += conv_to_char(im[p_vert][p_horz])
                p_horz += w_ratio
            p_vert += h_ratio
            line += "\n"
            print(line[:-1])


if __name__ == "__main__":
    t = TermIt()
    vc = cv2.VideoCapture(0)
    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
        while (rval):
            t.print_it(frame)
            rval, frame = vc.read()

