import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

class VideoPlayer(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)

    self.fps = 30
    self.video = None
    self.frame = None
    self.frame_num = 0
    self.frame_length = 0

    self.play_flg = False

    self.create_video_canvas()
    self.create_ctrl_panel()

  def create_video_canvas(self):
    self.video_canvas = tk.Canvas(self.master, width=640, height=480, bg='#000000')
    self.video_canvas.pack(fill='x', padx=30)
  
  def create_ctrl_panel(self):
    self.ctrl_panel = tk.Frame(self.master, width=640, height=50)
    self.create_play_button()
    self.create_seek_bar()
    self.ctrl_panel.pack(fill='x', padx=30)
  
  def create_seek_bar(self):
    self.scale_var = tk.DoubleVar()
    self.seek_bar = tk.Scale(
      self.ctrl_panel,
      variable = self.scale_var,
      command = self.slider_scroll,
      orient = tk.HORIZONTAL,
      length = 600,
      width = 20,
      sliderlength = 20,
      from_ = self.frame_num,
      to = self.frame_length,
      tickinterval = int(self.frame_length/5),
      troughcolor='#0000ff'
    )
    self.seek_bar.pack(side=tk.LEFT)
  
  def slider_scroll(self, event=None):
    self.play_flg = False
    self.play_button.config(text='▶')
    pos = self.scale_var.get()
    self.video.set(cv2.CAP_PROP_POS_FRAMES, pos)
    self.show_img()
  
  def create_play_button(self):
    self.play_button = tk.Button(self.ctrl_panel, text="▶", width=2, command=self.state_change)
    self.play_button.pack(side=tk.LEFT, padx=5)
  
  def state_change(self):
    self.play_flg = not self.play_flg
    if self.play_flg:
      self.play_button.config(text='ll')
    else:
      self.play_button.config(text='▶')
  
  def get_video(self, video_source=0):
    self.play_flg = False
    self.video = cv2.VideoCapture(video_source)
    self.fps = self.video.get(cv2.CAP_PROP_FPS)
    self.frame = None
    self.frame_num = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
    self.frame_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
    self.seek_bar.config(to=self.frame_length, tickinterval = int(self.frame_length/5))
  
  def next_frame(self):
    if not self.play_flg:
      return
    self.frame_num = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
    self.scale_var.set(self.frame_num)
    self.show_img()

  def show_img(self):
    ret, self.frame = self.video.read()
    if ret is False:
      self.play_flg = False
      self.play_button.config(text='▶')
      return
    rgb_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_img)
    pad_img = ImageOps.pad(pil_img, (640, 480))
    self.frame = ImageTk.PhotoImage(pad_img)
    self.video_canvas.create_image(640/2, 480/2,image=self.frame)
  
  def video_frame_timer(self):
    self.next_frame()
    self.master.after(int(1000/self.fps), self.video_frame_timer)

if __name__ == '__main__':
  root = tk.Tk()
  root.title('VideoPlayer')
  root.geometry('650x550')
  video_filepath = ''
  video_player = VideoPlayer(master=root)
  video_player.get_video(video_filepath)
  video_player.video_frame_timer()
  root.mainloop()