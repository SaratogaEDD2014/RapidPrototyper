import wx
import os

class BitmapViewer(wx.Panel):
    def __init__(self, parent, bitmaps=[], id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize):
        super(BitmapViewer, self).__init__(parent, id, pos, size)
        self.bmps = bitmaps
    def bitmaps_from_dir(self, directory):
        if os.path.exists(directory):
            for the_file in os.listdir(directory):
                if the_file.name.count('.bmp') != 0:
                    file_path = os.path.join(directory, the_file)
                    self.bmps.append(wx.Bitmap(file_path))

def main():
    pass

if __name__ == '__main__':
    main()
