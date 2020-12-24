from PIL import Image
import cv2
import os

gray_scale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
#gray_scale = " "

def conv_to_char(px):
    if len(px) > 1:
        mean = px.mean()
        ret = "\x1b[38;2;{};{};{}m".format(px[2], px[1], px[0])
    else:
        mean = px
        ret = ""
    ratio = mean / 255
    ratio = int(ratio * len(gray_scale))
    ret += gray_scale[ratio]
    return ret

class TermIt:
    def __init__(self):
        rows, cols = os.popen('stty size', 'r').read().split()
        self.rows = int(rows) * 90 // 100
        self.cols = int(cols) * 90 // 100

    def print_it(self, im):
        height = len(im)
        width = len(im[0])
        print("\033[0;0H")
        w_ratio = int(width / self.cols)
        h_ratio = int(height / self.rows)
        p_vert = 0
        while p_vert < height:
            p_horz = 0
            line = ""
            while p_horz < width:
                line += conv_to_char(im[p_vert][p_horz])
                p_horz += w_ratio
            print(line)
            p_vert += h_ratio


if __name__ == "__main__":
    #cv2.namedWindow("preview")
    t = TermIt()
    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
        while (rval):
            t.print_it(frame)
            rval, frame = vc.read()

