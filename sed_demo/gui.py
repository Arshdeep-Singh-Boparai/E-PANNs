#!/usr/bin python
# -*- coding:utf-8 -*-


"""
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


# ##############################################################################
# # HELPERS
# ##############################################################################
class ResponsiveImgCanvas(tk.Canvas):
    """
    Image that adapts to the width of its container.
    Based on: https://stackoverflow.com/a/22837522/4511978
    """

    def __init__(self, parent, img_path, margin_ratio=1.1, max_height=None,
                 **kwargs):
        """
        :param float margin_ratio: The height of the container will be the
          img height times this number.
        :param int max_height: If given, limits the img height
        """
        super().__init__(parent, **kwargs)
        # We need to keep a reference to the original image and size
        self.path = img_path
        self.ori_img = Image.open(img_path)
        self.ori_w, self.ori_h = self.ori_img.size
        self.margin_ratio = margin_ratio
        self.max_h = max_height
        # Then we get our resized copy and set it via create_image. Store
        # references for everything
        self.resized_img, _ = self.get_new_width(123)  # some dummy value
        self.img_on_canvas = self.create_image(
            0, 0, image=self.resized_img, anchor=tk.CENTER)
        # Whenever the parent frame changes size, on_resize will be called
        self.bind("<Configure>", self.on_resize)

    def get_new_width(self, new_w, max_h=None):
        """
        """
        # first assume new W and update H
        new_h = round((float(new_w) / self.ori_w) * self.ori_h)
        if max_h is not None and new_h > max_h:
            # if H surpassed max_h, assume max H and update W
            new_h = max_h
            new_w = round((float(new_h) / self.ori_h) * self.ori_w)
        # resize image and return it
        img = self.ori_img.resize((new_w, new_h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img, (new_w, new_h)

    def on_resize(self, event):
        """
        """
        self.resized_img, (_, new_h) = self.get_new_width(event.width, self.max_h)
        # Find the new "centered" position and replace image
        self.delete(self.img_on_canvas)
        self.img_on_canvas = self.create_image(
            event.width / 2, new_h / 2, image=self.resized_img, anchor=tk.CENTER)
        self.config(height=round(new_h * self.margin_ratio))


class ResponsiveImgBar(ttk.Frame):
    """
    """

    def __init__(self, parent, img_paths, max_height=None, img_pad=0, bg=None):
        """
        """
        super().__init__(parent)
        self.paths = img_paths
        self.N = len(img_paths)
        self.imgs = [ResponsiveImgCanvas(
            self, lp, max_height=max_height, bd=0, bg=bg,
            highlightthickness=0) for lp in img_paths]
        for i, img in enumerate(self.imgs):
            # img.pack(side="left", expand=True)  # , fill="both")
            img.grid(row=0, column=i, padx=img_pad, pady=img_pad)
            self.columnconfigure(i, weight=1)


# ##############################################################################
# # GUI FRONTEND
# ##############################################################################
class DemoFrontend(tk.Tk):
    """
    This class implements the set of responsive widgets and layouts used in
    the demo. It also provides state control and access points for the
    Start/Stop and Exit buttons, whose functionality can be overriden by
    extending the ``start(), stop(), exit()`` methods respectively.
    """

    TITLE = "Live Sound Recognition using Efficient PANNs (E-PANNs)"
    START_BUTTON_TEXT = "Start"
    STOP_BUTTON_TEXT = "Stop"
    EXIT_BUTTON_TEXT = "Exit"

    BG_COLOR = "#ffffff"
    BUTTON_COLOR = "#aaaaaa"

    BAR_STYLE = "bar.Horizontal.TProgressbar"
    BAR_COLOR = "#aaaaff"
    BAR_BG_COLOR = "#aaffaa"

    def __init__(self, top_k, top_banner_path, logo_paths=[],
                 max_top_banner_h=120, max_logos_h=35, margin=20):
        """
        """
        super().__init__()
        self.title(self.TITLE)
        self.top_k = top_k
        self.top_banner_path = top_banner_path
        self.logo_paths = logo_paths

        # create global layout in 3 areas:
        self.top_area, self.top_widgets = self.get_top_area(
            max_top_banner_h, padding=(margin, margin, margin, 0))  # ltrb
        self.top_area.grid(row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        #
        self.mid_area, self.mid_widgets = self.get_mid_area(
            top_k, padding=(margin, 0, margin, 0))
        self.mid_area.grid(row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        #
        self.bottom_area, self.bottom_widgets = self.get_bottom_area(
            max_logos_h, img_padding=margin)
        self.bottom_area.grid(row=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        # distribute space for the 3 areas
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)  # mid block has 4/6 of the height
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # distribute space within each area
        self.top_area.rowconfigure(1, weight=1)
        self.top_area.rowconfigure(2, weight=1)

        self.mid_area.rowconfigure(0, weight=1)

        self.bottom_area.rowconfigure(0, weight=1)
        self.bottom_area.rowconfigure(1, weight=1)
        #
        for i in [1]:  #  range(3):
            self.top_area.columnconfigure(i, weight=1)
            self.mid_area.columnconfigure(i, weight=1)
            self.bottom_area.columnconfigure(i, weight=1)

        # Wire the start/exit buttons with the methods
        self.start_b = self.top_widgets["start_but"]
        self.exit_b = self.bottom_widgets["exit_but"]
        self.start_b["command"] = self.dispatch_start
        self.exit_b["command"] = self.exit_demo
        #
        self.sound_labels = self.mid_widgets["sounds"]
        self.confidence_bars = self.mid_widgets["confidences"]

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure("suptitle.TLabel", font=("Helvetica", 25, "bold"),
                             background=self.BG_COLOR)

        self.style.configure("title.TLabel", font=("Helvetica", 20, "bold"),
                             background=self.BG_COLOR)

        self.style.configure("TLabel", font=("Helvetica", 18),
                             background=self.BG_COLOR)
        self.style.configure("TButton", font=("Helvetica", 18),
                             borderwidth=1,
                             background=self.BUTTON_COLOR)
        self.style.configure("TFrame", background=self.BG_COLOR)
        self.style.configure("TCanvas", background=self.BG_COLOR)
        self.style.configure(self.BAR_STYLE, relief="sunken",
                             # throughcolor="red",
                             # bordercolor="red",
                             # darkcolor="red",
                             # lightcolor="red",
                             background=self.BAR_COLOR)  # self.BAR_BG_COLOR, relief="sunken")

        # ("entryConf.Horizontal.TProgressbar", foreground='black', background='#7d89af',
        #                     troughcolor='white',relief='sunken')

    def get_top_area(self, max_img_h=150, padding=(0, 0, 0, 0)):
        """
        """
        top_area = ttk.Frame(self, padding=padding)
        #
        top_canvas = ResponsiveImgCanvas(
            top_area, self.top_banner_path, max_height=max_img_h,
            bd=0, highlightthickness=0, bg=self.BG_COLOR)
        title_lbl = ttk.Label(top_area, text=self.TITLE, style="suptitle.TLabel")
        start_but = ttk.Button(top_area, text=self.START_BUTTON_TEXT)
        top_canvas.grid(row=0, column=0, columnspan=3, sticky=(tk.N, tk.S, tk.E, tk.W))
        title_lbl.grid(row=1, column=0, columnspan=3)
        start_but.grid(row=2, column=0, columnspan=3)
        #
        widgets = {"top_canvas": top_canvas, "title_lbl": title_lbl,
                   "start_but": start_but}
        return top_area, widgets

    def get_mid_area(self, num_items, padding=(0, 0, 0, 0)):
        """
        """
        mid_area = ttk.Frame(self, padding=padding)
        # populate header labels
        rank_lbl = ttk.Label(mid_area, text="Rank", style="title.TLabel")
        sound_lbl = ttk.Label(mid_area, text="Sound", style="title.TLabel")
        confidence_lbl = ttk.Label(mid_area, text="Confidence", style="title.TLabel")
        rank_lbl.grid(row=0, column=0, columnspan=1)
        sound_lbl.grid(row=0, column=1, columnspan=1)
        confidence_lbl.grid(row=0, column=2, columnspan=1)
        #
        ranks, sounds, confidences = [], [], []
        for i in range(1, num_items + 1):
            rank = ttk.Label(mid_area, text=f"{i}")
            sound = ttk.Label(mid_area, text="")
            # confidence = ttk.Button(mid_area, text="confidence bar")
            confidence = ttk.Progressbar(
                mid_area, style=self.BAR_STYLE, orient="horizontal", mode="determinate", maximum=1,
                value=0.0)
            #
            rank.grid(row=i, column=0, columnspan=1)
            sound.grid(row=i, column=1, columnspan=1)
            confidence.grid(row=i, column=2, columnspan=1)
            #
            ranks.append(rank)
            sounds.append(sound)
            confidences.append(confidence)
        #
        bottom_slack = ttk.Frame(mid_area, padding=(0, 0, 0, 0))
        bottom_slack.grid(row=num_items+1, column=0, columnspan=3,
                          sticky=(tk.N, tk.S, tk.E, tk.W))
        mid_area.rowconfigure(num_items+1, weight=1)
        #
        widgts = {"labels": [rank_lbl, sound_lbl, confidence_lbl],
                  "ranks": ranks, "sounds": sounds, "confidences": confidences}
        return mid_area, widgts

    def get_bottom_area(self, max_logos_h=50, img_padding=0):
        """
        """
        bottom_area = ttk.Frame(self)
        #
        exit_but = ttk.Button(bottom_area, text=self.EXIT_BUTTON_TEXT)
        logo_bar = ResponsiveImgBar(bottom_area, self.logo_paths, max_logos_h,
                                    img_padding, bg=self.BG_COLOR)
        #
        exit_but.grid(row=0, column=0, columnspan=3)
        logo_bar.grid(row=1, column=0, columnspan=3,
                      sticky=tk.S)
        #
        widgets = {"exit_but": exit_but, "logo_bar": logo_bar}
        return bottom_area, widgets


    def is_running(self):
        """
        """
        state = self.start_b["text"]
        is_running = (state == self.STOP_BUTTON_TEXT)
        return is_running

    def toggle_start(self):
        """
        """
        if self.is_running():
            self.start_b["text"] = self.START_BUTTON_TEXT
        else:
            self.start_b["text"] = self.STOP_BUTTON_TEXT

    def dispatch_start(self):
        """
        Depending on the current state when the start/stop button is pressed,
        this dispatcher method calls either ``start()`` or ``stop()``.
        """
        was_running = self.is_running()
        self.toggle_start()
        if was_running:
            self.stop()
        else:
            self.start()

    def start(self):
        """
        Implement this method to start the demo.
        """
        print("Started!")

    def stop(self):
        """
        Implement this method to stop the demo temporarily.
        """
        print("Stopped!")

    def exit_demo(self):
        """
        Implement this method to exit the demo permanently.
        """
        print("Exit pressed")
