#coding:utf-8
 
import wx
import os 
from PIL import Image
 
import entry


FRAME_SIZE = (800, 600)
IMAGE_PANEL_SIZE = (300, 300)
DIALOG_SIZE = (200, 100)
BUTTON_DEFAULT_SIZE = (50, 20)


class Dialog(wx.Dialog):
    def __init__(self, parent, title):
        super(Dialog, self).__init__(parent, title=title, size=DIALOG_SIZE,
            pos=(FRAME_SIZE[0]/2, FRAME_SIZE[1]/2))
        panel = wx.Panel(self)
        self.btn = wx.Button(panel, wx.ID_OK, label="确认", size=BUTTON_DEFAULT_SIZE, pos=(75, 50))

 
class FileDialog(wx.Frame):
 
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self,None, -1, size=FRAME_SIZE)
        button_choose_image = wx.Button(self, -1, u"选择图片",(520,100))
        self.Bind(wx.EVT_BUTTON, self.on_button_choose_image, button_choose_image)
        
        button_entry = wx.Button(self, -1, u"录入数据",(380,500))
        self.Bind(wx.EVT_BUTTON, self.on_button_entry, button_entry)

        static_text_name = wx.StaticText(self, -1, u'名字', (100, 100), style=wx.ALIGN_CENTER)
        self.input_text_name = wx.TextCtrl(self, -1, u'', size=(80, 20), pos=(150, 100))

        self.path = None
        self.image_panel = wx.Panel(self,-1, size=IMAGE_PANEL_SIZE, pos=(420, 150))

    def on_button_choose_image(self, event):

        file_dialog = wx.FileDialog(self,message=u"选择图片",
                            defaultDir=os.getcwd(),
                            defaultFile="",
                            style=wx.FD_OPEN|wx.FD_CHANGE_DIR)

        if file_dialog.ShowModal() == wx.ID_OK:
            paths = file_dialog.GetPaths()
            if len(paths) > 0:
                self.path = paths[0]

        file_dialog.Destroy()

        if self.path is None:
            return

        self.image_panel.DestroyChildren()
        image = wx.Image(self.path, wx.BITMAP_TYPE_ANY)
        scaled_image = self.scale_image(image)
        wx.StaticBitmap(self.image_panel, -1, wx.BitmapFromImage(scaled_image))

    def on_button_entry(self, event):
        if self.path is None:
            Dialog(self, "请选择图片").Show()
            return

        name = self.input_text_name.GetValue()
        if not name:
            Dialog(self, "请输入名字").Show()
            return

        e = entry.Entry()
        ret = e.load_image(self.path, name)
        if ret == -1:
            Dialog(self, "图片不存在").Show()
        elif ret == -2:
            Dialog(self, "图片已存在").Show()
        elif ret == -3:
            Dialog(self, "未识别出人脸").Show()

    def scale_image(self, image):
        width, height = image.GetWidth(), image.GetHeight()
        max_dim = max(width, height)
        new_width = 1.0 * IMAGE_PANEL_SIZE[0] * width / max_dim
        new_height = 1.0 * IMAGE_PANEL_SIZE[0] * height / max_dim
        return image.Scale(new_width, new_height)


if __name__ == '__main__':
    frame = wx.PySimpleApp()
    app = FileDialog()
    app.Show()
    frame.MainLoop()
