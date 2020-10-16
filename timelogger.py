
#time logger

import datetime
import os
import wx
#import matplotlib
#matplotlib.use('agg')
import matplotlib.pyplot as plt
from collections import OrderedDict

# settings
cwd = os.getcwd()
save_location = os.path.join(cwd, "testlog.txt")
graph_path = os.path.join(cwd, "graph.png")
key_press_dict = {} # letter = time of key press

key_times_dict = {} # letter = list of time down, time up

# The app
class timelog(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Time logger")

        self.stopwatch = wx.StopWatch()
        self.stopwatch.Pause()
        self.stop_switch = 0

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.recuring_events_lc = wx.ListCtrl(self, size=(-1, 600), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.recuring_events_lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick_recuring)
        #self.recuring_events_lc.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        #self.recuring_events_lc.Bind(wx.EVT_KEY_UP, self.onkey_up)
        self.recuring_events_lc.InsertColumn(0, 'Action')
        self.recuring_events_lc.SetColumnWidth(0, 250)
        self.recuring_events_lc.InsertColumn(1, 'button')
        self.recuring_events_lc.InsertColumn(2, 'count')
        self.recuring_events_lc.InsertColumn(3, 'duration')
        self.recuring_events_lc.SetColumnWidth(3, 150)
        # buttons
        self.save_btn = wx.Button(self, label='Save')
        self.save_btn.Bind(wx.EVT_BUTTON, self.save_click)
        self.load_btn = wx.Button(self, label='Load')
        self.load_btn.Bind(wx.EVT_BUTTON, self.load_click)
        self.clear_btn = wx.Button(self, label='Clear')
        self.clear_btn.Bind(wx.EVT_BUTTON, self.clear_click)
        self.graph_btn = wx.Button(self, label='Graph')
        self.graph_btn.Bind(wx.EVT_BUTTON, self.graph_click)
        # timing options
        timing_opts = ['seconds', 'date']
        self.tiimg_style_cb = wx.ComboBox(self, choices = timing_opts, value="seconds", size=(200, 40))
        # timing icon
        timer_stopped_path = os.path.join(cwd, "timer_stop.png")
        timer_paused_path  = os.path.join(cwd, "timer_pause.png")
        timer_running_path = os.path.join(cwd, "timer_start.png")
        self.timer_icon_stop  = wx.Image(timer_stopped_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.timer_icon_pause = wx.Image(timer_paused_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.timer_icon_run   = wx.Image(timer_running_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.timing_icon = wx.BitmapButton(self, -1, self.timer_icon_stop, size=(40, 40))
        self.timing_icon.Bind(wx.EVT_BUTTON, self.timing_icon_click)
        # graphs
        self.graph_space = wx.BitmapButton(self, -1, size=(600, 600))

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_sizer.Add(self.save_btn, 0, wx.ALL|wx.EXPAND, 3)
        buttons_sizer.Add(self.load_btn, 0, wx.ALL|wx.EXPAND, 3)
        buttons_sizer.Add(self.clear_btn, 0, wx.ALL|wx.EXPAND, 3)
        buttons_sizer.AddStretchSpacer(1)
        buttons_sizer.Add(self.graph_btn, 0, wx.ALL|wx.EXPAND, 3)

        timing_sizer = wx.BoxSizer(wx.HORIZONTAL)
        timing_sizer.Add(self.tiimg_style_cb, 0, wx.ALL|wx.EXPAND, 3)
        timing_sizer.Add(self.timing_icon, 0, wx.ALL, 3)
        self.left_sizer =  wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.Add(buttons_sizer, 0, wx.ALL|wx.EXPAND, 3)
        self.left_sizer.Add(timing_sizer, 0, wx.ALL|wx.EXPAND, 3)
        #self.main_sizer.AddStretchSpacer(1)
        self.left_sizer.Add(self.recuring_events_lc, 0, wx.ALL|wx.EXPAND, 3)
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.Add(self.graph_space, 0, wx.ALL|wx.EXPAND, 3)

        self.main_sizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.left_sizer, 0, wx.ALL|wx.EXPAND, 3)
        self.main_sizer.Add(self.right_sizer, 0, wx.ALL|wx.EXPAND, 3)
        self.SetSizer(self.main_sizer)

        # delcairing variables
        self.test_time = 1


    def onDoubleClick_recuring(self, e):
        index =  e.GetIndex()

        key = self.recuring_events_lc.GetItem(index, 1).GetText()
        msg = "Set name for " + key + " key log"
        action_name_dialog = wx.TextEntryDialog(self, msg, "Select action to bind", "")
        if action_name_dialog.ShowModal() == wx.ID_OK:
            action_name = action_name_dialog.GetValue()
            self.recuring_events_lc.SetItem(index, 0, action_name)

    def add_to_times_dict(self, direction, key, time):
        if key in key_times_dict:
            keys_list = key_times_dict[key]
            keys_list = keys_list + [[direction, time]]
        else:
            keys_list = [[direction, time]]
        key_times_dict[key] = keys_list

    def add_to_table(self, keycode, duration):
        item_index = -1
        count = 1
        # check if exists
        for index in range(0, self.recuring_events_lc.GetItemCount()):
            key = self.recuring_events_lc.GetItem(index, 1).GetText()
            if str(key) == str(keycode):
                item_index = index

        if item_index == -1:
            item_index = self.recuring_events_lc.GetItemCount()
            self.recuring_events_lc.InsertItem(item_index, "none")
        else:
            count = int(self.recuring_events_lc.GetItem(item_index, 2).GetText()) + 1
            try:
                duration = duration + float(self.recuring_events_lc.GetItem(item_index, 3).GetText())
            except:
                duration = duration    
        #
        self.recuring_events_lc.SetItem(item_index, 1, str(keycode))
        self.recuring_events_lc.SetItem(item_index, 2, str(count))
        self.recuring_events_lc.SetItem(item_index, 3, str(duration))
        #
        #if keycode in key_times_dict:
        #    print(key_times_dict[keycode])

    def onkey_up(event):
        self = frame
        # Ignore space bar
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            return None
        # Letters
        keyucode = event.GetUnicodeKey()
        if keyucode != wx.WXK_NONE:
            letter = ("%c"%keyucode)
            press_time = key_press_dict[letter]
            if self.tiimg_style_cb.GetValue() == "date":
                time = datetime.datetime.now()
            else:
                time = self.get_timer_time()

            duration = time - press_time
            self.add_to_times_dict("U", letter, time)
            self.add_to_table(letter, duration)

    def timing_icon_click(self, e):
        if self.stop_switch == 0:
            self.stopwatch.Start()
            self.stop_switch = 1
            self.timing_icon.SetBitmap(self.timer_icon_run)
            print(" Started ")
        elif self.stop_switch == 1:
            self.stopwatch.Pause()
            self.stop_switch = 2
            self.timing_icon.SetBitmap(self.timer_icon_pause)
            print(" Paused ")
        elif self.stop_switch == 2:
            self.stopwatch.Resume()
            self.stop_switch = 1
            self.timing_icon.SetBitmap(self.timer_icon_run)
            print("Resumed")

    def onKeyPress(event):
        self = frame
        # start and stop timer with space key
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_SPACE:
            if self.stop_switch == 0:
                self.stopwatch.Start()
                self.stop_switch = 1
                self.timing_icon.SetBitmap(self.timer_icon_run)
            elif self.stop_switch == 1:
                self.stopwatch.Pause()
                self.stop_switch = 2
                self.timing_icon.SetBitmap(self.timer_icon_pause)
            elif self.stop_switch == 2:
                self.stopwatch.Resume()
                self.stop_switch = 1
                self.timing_icon.SetBitmap(self.timer_icon_run)
            return None
        #
        if self.stop_switch == 0:
            self.stopwatch.Start(0)
            self.stop_switch = 1
            self.timing_icon.SetBitmap(self.timer_icon_run)
            print(" Started ")
        elif self.stop_switch == 2:
            self.stopwatch.Resume()
            self.stop_switch = 1
            self.timing_icon.SetBitmap(self.timer_icon_run)
            print("Resumed")

        # handle letters
        keyucode = event.GetUnicodeKey()
        if keyucode != wx.WXK_NONE:
            letter = ("%c" %keyucode)
            # ignore key repeats from keyboard
            if letter in key_times_dict:
                if key_times_dict[letter][-1][0] == "D":
                    return None
            #
            if self.tiimg_style_cb.GetValue() == "date":
                time = datetime.datetime.now()
            else:
                time = self.get_timer_time()
            key_press_dict[letter] = time
            self.add_to_times_dict("D", letter, time)
            #self.add_to_table("'%c'"%keyucode)
        event.Skip()

    def get_timer_time(self):
        #self.test_time = self.test_time + 1
        return self.stopwatch.Time() / 1000


    def get_name(self, letter):
        last_index = self.recuring_events_lc.GetItemCount()
        if not last_index == 0:
            for index in range(0, last_index):
                name = self.recuring_events_lc.GetItem(index, 1).GetText()
                if name == letter:
                    return self.recuring_events_lc.GetItem(index, 0).GetText()

    def save_click(self, e):
        file_text = "# Timing file for timing log program script thing\n"
        file_text += "#timeing_method=" + self.tiimg_style_cb.GetValue()
        for key, value in list(key_times_dict.items()):
            letter = key
            name = self.get_name(letter)
            time_list = value
            line_text = name + ">" + letter + ">"
            for item in time_list:
                line_text = line_text + str(item[0]) + "=" + str(item[1]) + ","
            file_text = file_text + "\n" + line_text
        # save to file
        with open(save_location, "w") as f:
            f.write(file_text)
        print(" Saved to " + save_location)

    def load_click(self, e):
        timeing_method="date"
        with open(save_location, "r") as f:
            file_text = f.read()
        file_text = file_text.splitlines()
        item_index = 0
        self.clear_click("e")
        for line in file_text:
            if not line.strip()[:1] == "#":
                name, key, data = line.split(">")
                data = data.split(",")
                print(name, key, len(data))
                # dictionarys
                data_list = []
                for item in data:
                    item = item.split("=")
                    #print (item)
                    if len(item) == 2:
                        datetime_text = item[1]
                        if timeing_method == "date":
                            date_time = datetime.datetime.strptime(datetime_text, '%Y-%m-%d %H:%M:%S.%f')
                        elif timeing_method == "seconds":
                            date_time = float(datetime_text)
                        data_list = data_list + [ [ item[0], date_time ] ]
                key_times_dict[key] = data_list
                # table
                self.recuring_events_lc.InsertItem(item_index, name)
                self.recuring_events_lc.SetItem(item_index, 1, str(key))
                self.recuring_events_lc.SetItem(item_index, 2, str( int(len(data_list) /2)))
                self.recuring_events_lc.SetItem(item_index, 3, "--")

                item_index = item_index + 1
            elif "timeing_method=" in line:
                timeing_method = line.split("#timeing_method=")[1].strip()
                print(" Loading using timing method " + timeing_method)

    def clear_click(self, e):
        key_times_dict.clear()
        key_press_dict.clear()
        self.recuring_events_lc.DeleteAllItems()
        self.stop_switch = 0
        self.stopwatch.Pause()
        self.timing_icon.SetBitmap(self.timer_icon_stop)


    def graph_click(self, e):
        show_up = True # graph when the button is raised also
        layering = "sequential" # "sequential" or "alphabet" alphabet leaves spaces for missing letters
        #print(" ")
        #print(" - Graph - ")
        #print(" ")
        #
        size_h = 11
        size_v = 11
        fig, ax = plt.subplots(figsize=(size_h, size_v))
        #

        layer = 0
        test_dic = OrderedDict(sorted(key_times_dict.items()))
        for key, value in list(test_dic.items()):
            letter = key
            if layering == "sequential":
                layer = layer + 1
            elif layering == "alphabet":
                layer = ord(key)
            time_list = value
            value_list = []
            date_list  = []
            for item in time_list:
                if item[0] == "D":
                    value_list.append(layer)
                    date_list.append(item[1])
                    if show_up == True:
                        value_list.append(layer + 1)
                        date_list.append(item[1])
                elif item[0] == "U":
                    if show_up == True:
                        value_list.append(layer + 1)
                        date_list.append(item[1])
                        value_list.append(layer)
                        date_list.append(item[1])
            # make graph
            ax.plot(date_list, value_list, label=letter, lw=1)
            #print("letter " + letter + " " + str(len(value_list)) + " " + str(len(date_list)))

        ax.xaxis_date()
        #fig.autofmt_xdate()
        ax.legend()
        #plt.show()
        plt.savefig(graph_path)
        # tidy up after ourselves
        plt.close(fig)
        print(" Graph saved to " + graph_path)
        self.show_local_graph(graph_path)

    def show_local_graph(self, graph_path):
        image_to_show = wx.Image(graph_path, wx.BITMAP_TYPE_ANY)
        image_to_show = self.scale_pic(image_to_show, 600)
        self.graph_space.SetBitmap(image_to_show.ConvertToBitmap())

    def scale_pic(self, pic, target_size):
        pic_height = pic.GetHeight()
        pic_width = pic.GetWidth()
        # scale the image, preserving the aspect ratio
        if pic_width > pic_height:
            sizeratio = (pic_width / target_size)
            new_height = (pic_height / sizeratio)
            scale_pic = pic.Scale(target_size, new_height, wx.IMAGE_QUALITY_HIGH)
        else:
            sizeratio = (pic_height / target_size)
            new_width = (pic_width / sizeratio)
            scale_pic = pic.Scale(new_width, target_size, wx.IMAGE_QUALITY_HIGH)
        return scale_pic




# Run the program
if __name__ == "__main__":
    app = wx.App()
    frame = timelog()
    frame.Centre()
    frame.Fit()
    app.Bind(wx.EVT_KEY_DOWN, timelog.onKeyPress)
    app.Bind(wx.EVT_KEY_UP, timelog.onkey_up)
    frame.Show()
    app.MainLoop()
