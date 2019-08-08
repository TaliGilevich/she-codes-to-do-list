from sys import version
from sqlite3 import sqlite_version
from tkinter import Tk, TkVersion, Toplevel, Frame, Grid, Canvas, PhotoImage, Entry, Text, Label, Button, StringVar, WORD, END, RIGHT, LEFT, BOTH, X, E, W
from tkinter import messagebox
from tkinter.ttk import Combobox, Sizegrip

from CommonDefinitions import msgboard_img_path, justdoit_img_path, colornotes_img_path, notes_dict, notes_views_lst, prrt2color_dict, notes_to_display_lst, category_filter_ctrlvar, descr_filter_ctrlvar
from GeneralFunctions import clean_display, aux_filter_notes, highlight_match, init, terminate
from DBOperations import category_names_lst, priority_names_lst, db_insert_note, db_delete_note, db_update_note

from NotePureData_classdef import NotePureData
from Calendar_classdef import Calendar

print(f'Python version: {version}')  #sys.version
print(f'SQLite3 version: {sqlite_version}') #sqlite3.sqlite_version
print(f'TKinter version: {TkVersion}')

def display_notes(event=None):
    """This function is responsible for displaying the notes"""
    clean_display()
    notes_views_lst.clear()

    # building list of objects of type NoteView (i.e. graphic representation of a note)
    notes_views_lst.extend([highlight_match(note_view, descr_filter_ctrlvar.get()) for note_view in [NoteView(frm_root.cnvs_notes_display, note_obj) for note_obj in notes_to_display_lst]])

    for seqnum, nv in enumerate(notes_views_lst):
        nv.grid(row=seqnum // frm_root.cnvs_notes_display.gridcols_cnt,  column=seqnum % frm_root.cnvs_notes_display.gridcols_cnt, padx=frm_root.note_padding, pady=frm_root.note_padding)


def action_new_note_dialog(event):
    """ NewNoteDialog command (New Note dialog is opened by click on the 'newnote' button)"""
    dlg_new_note = Toplevel(root)
    dlg_new_note.title('New Note')

    dlg_new_note.geometry('250x250+250+250')
    NewNoteFrame(dlg_new_note)

# frame of the New Note dialog
class NewNoteFrame(Frame):
    """"Window that provides UI(input fields and buttons) necessary for creating new note
    Derives from class Frame"""

    # class variables
    ipadx_val = 1
    ipady_val = 10
    label_font = '"Century Gothic" 10 bold'
    lbl_ctgr_text = 'Category:'
    lbl_dscr_text = 'Description:'
    lbl_date_text = 'Date:'
    lbl_prrt_text = 'Priority:'
    data_font = '"Segoe Print" 11'
    btn_width = 6
    btn_conf_text = 'Confirm'
    btn_cancel_text = 'Cancel'
    btn_font = 'Arial 9'
    btn_padx = 25
    btn_pady = 35

    def __init__(self, master):
        """ctor"""
        super().__init__(master)
        self.pack(fill=BOTH, expand=True)

        # setting default priority to Normal, corresponding background color is lightyellow
        bgcolor = prrt2color_dict[priority_names_lst[1]]  # 'Normal':'lightyellow'
        self.create_widgets(master, bgcolor)

    def create_widgets(self, master, bg_color):
        """This method defines UI of the New Note window"""
        self.frm_main_newnote = Frame(self, bg=bg_color)
        self.frm_main_newnote.pack(fill=BOTH)

        self.lbl_category = Label(self.frm_main_newnote, bg=bg_color, font=__class__.label_font, text=__class__.lbl_ctgr_text)
        self.lbl_category.grid(row=0, column=0, sticky=W, ipadx=__class__.ipadx_val, ipady=__class__.ipady_val)

        self.cmbx_category = Combobox(self.frm_main_newnote, width=12, font=__class__.data_font)  # ttk.Combobox
        self.cmbx_category.configure(values=category_names_lst)  # the values are: Personal, College, Work, Home
        self.cmbx_category.current(0)  # i.e. default value is 'Personal'
        self.cmbx_category.grid(row=0, column=1, columnspan=2, sticky=W, ipadx=__class__.ipadx_val)

        self.lbl_description = Label(self.frm_main_newnote, bg=bg_color, font=__class__.label_font, text=__class__.lbl_dscr_text)
        self.lbl_description.grid(row=2, column=0, sticky=W, ipadx=__class__.ipadx_val, ipady=__class__.ipady_val)

        self.entry_description = Entry(self.frm_main_newnote, width=14, font=__class__.data_font)
        self.entry_description.grid(row=2, column=1, columnspan=2, sticky=W, ipadx=__class__.ipadx_val)

        self.lbl_date = Label(self.frm_main_newnote, bg=bg_color, font=__class__.label_font, text=__class__.lbl_date_text)
        self.lbl_date.grid(row=4, column=0, sticky=W, ipadx=__class__.ipadx_val, ipady=__class__.ipady_val)

        self.entry_date = Entry(self.frm_main_newnote, width=14, font=__class__.data_font)
        self.entry_date.grid(row=4, column=1, columnspan=2, sticky=W, ipadx=__class__.ipadx_val)

        self.lbl_priority = Label(self.frm_main_newnote, bg=bg_color, font=__class__.label_font, text=__class__.lbl_prrt_text)
        self.lbl_priority.grid(row=6, column=0, sticky=W, ipadx=__class__.ipadx_val, ipady=__class__.ipady_val)

        self.cmbx_priority = Combobox(self.frm_main_newnote, width=12, font=__class__.data_font)  # ttk.Combobox
        self.cmbx_priority.configure(values=priority_names_lst)  # the values are: High, Normal, Low
        self.cmbx_priority.current(1)  # i.e. default value is 'Normal'
        self.cmbx_priority.bind("<<ComboboxSelected>>", self.action_priority2bgcolor)
        self.cmbx_priority.grid(row=6, column=1, columnspan=2, sticky=W, ipadx=__class__.ipadx_val)

        btn_confirm = Button(self.frm_main_newnote, font=__class__.btn_font, width=__class__.btn_width, text=__class__.btn_conf_text, command=master.destroy)  # master is NewNote dialog
        btn_confirm.bind('<Button-1>', self.action_add_note)
        btn_confirm.grid(row=8, column=1, sticky=E, padx=__class__.btn_padx, pady=__class__.btn_pady)

        self.btn_cancel = Button(self.frm_main_newnote, font=__class__.btn_font, width=__class__.btn_width, text=__class__.btn_cancel_text, command=master.destroy)  # master = dlgNewNote  #self.frm_buttons_view
        self.btn_cancel.grid(row=8, column=2, sticky=W, pady=__class__.btn_pady)

    def action_add_note(self, event):
        """This method registers new note;
        activated by click on button Confirm"""
        # reading note details from UI
        category_str = self.cmbx_category.get().strip()
        descr_str = self.entry_description.get().strip()
        date_str = self.entry_date.get().strip()
        priority_str = self.cmbx_priority.get().strip()

        new_note_obj = NotePureData(category_str, descr_str, date_str, priority_str)  # object of class NotePureData
        notes_dict[new_note_obj.id] = new_note_obj  # adding new note object to the notes dictionary
        aux_filter_notes(category_filter_ctrlvar.get(), descr_filter_ctrlvar.get())

        display_notes()
        db_insert_note(new_note_obj)  # adding new note to the database

    def action_priority2bgcolor(self, event):
        """This method defines background color of the frame according to currently selected priority;
        activated by selection of a value from the Priority combo-box"""
        priority = self.cmbx_priority.get()

        # setting value of the background color according to the current task priority
        bgcolor = prrt2color_dict[priority]  # {'Low':'lightgreen', 'Normal':'lightyellow', 'High':'lightpink'}

        # setting background color of the NewNote frame and of the relevant widgets
        self.frm_main_newnote.configure(bg=bgcolor)
        widgets_lst = [w for w in self.frm_main_newnote.winfo_children() if isinstance(w, Label)]
        for w in widgets_lst:
            w.configure(bg=bgcolor)


class NoteView(Frame):
    """This class defines objects that display a single note
    Provides UI(fields and buttons) for displaying, updating / deleting a note
    Derives from class Frame
    """

    # class variables
    ipadx_val = 1
    pady_val = 15

    label_font = '"Curlz MT" 12 bold'
    data_font = '"Segoe Print" 12'

    lbl_kind_text = 'kind:'
    lbl_what_text = 'what:'
    lbl_when_text = 'when:'
    lbl_rush_text = "what's the rush:  "

    # TBD: images
    btn_font = 'Forte'
    btn_confirm_fg = 'green'
    btn_confirm_text = 'V'
    btn_remove_fg = 'red'
    btn_remove_text = 'X'

    def __init__(self, parent_frame, note_obj):
        """ctor"""
        bgcolor = prrt2color_dict[note_obj.priority]  # {'Low':'lightgreen', 'Normal':'lightyellow', 'High':'lightpink'}
        super().__init__(parent_frame, bg=bgcolor)

        self.note_dbid = note_obj.id  # TBD: note_obj.id - proper getter

        # control variables
        # task category
        self.ctgr_ctrlvar = StringVar()
        self.ctgr_ctrlvar.set(note_obj.category)

        # task description
        self.dscr_ctrlvar = StringVar()
        self.dscr_ctrlvar.set(note_obj.description)

        # date
        self.date_ctrlvar = StringVar()
        self.date_ctrlvar.set(note_obj.date)

        # task priority
        self.prrt_ctrlvar = StringVar()
        self.prrt_ctrlvar.set(note_obj.priority)

        self.create_widgets(bgcolor)

    def create_widgets(self, bg_color):
        """This method defines UI of the NoteView"""
        self.btn_confirm_update = Button(self, borderwidth=0, bg=bg_color, font=self.__class__.btn_font, fg=self.__class__.btn_confirm_fg, text=self.__class__.btn_confirm_text)
        self.btn_confirm_update.grid(row=0, column=1, sticky=E)
        self.btn_confirm_update.bind('<Button-1>', self.action_update_note)

        self.btn_remove_note = Button(self, borderwidth=0, bg=bg_color, font=self.__class__.btn_font, fg=self.__class__.btn_remove_fg, text=self.__class__.btn_remove_text)
        self.btn_remove_note.grid(row=0, column=2, sticky=E)
        self.btn_remove_note.bind('<Button-1>', self.action_remove_note)

        self.lbl_kind = Label(self, bg=bg_color, font=self.__class__.label_font, text=self.__class__.lbl_kind_text)
        self.lbl_kind.grid(row=2, column=0, sticky=W, pady=__class__.pady_val)
        self.entry_note_category = Entry(self, width=6, bg=bg_color, borderwidth=0, font=self.__class__.data_font, text=self.ctgr_ctrlvar)
        self.entry_note_category.bind('<Tab>', self.action_fix_category)  # may be will change back from '<Tab>' to '<Return>'
        self.entry_note_category.grid(row=2, column=1, sticky=W, pady=__class__.pady_val)

        self.lbl_what = Label(self, bg=bg_color, font=self.__class__.label_font, text=self.__class__.lbl_what_text)
        self.lbl_what.grid(row=3, column=0, sticky=W, pady=__class__.pady_val)
        self.text_note_descr = Text(self, height=1, width=10, wrap=WORD, bg=bg_color, borderwidth=0, font=self.__class__.data_font)
        self.text_note_descr.insert(END, self.dscr_ctrlvar.get())
        self.text_note_descr.grid(row=3, column=1, sticky=W, pady=__class__.pady_val)

        self.lbl_when = Label(self, bg=bg_color, font=self.__class__.label_font, text=self.__class__.lbl_when_text)
        self.lbl_when.grid(row=4, column=0, sticky=W, ipady=__class__.pady_val)
        self.entry_note_date = Entry(self, width=6, bg=bg_color, borderwidth=0, font=self.__class__.data_font, text=self.date_ctrlvar)
        self.entry_note_date.grid(row=4, column=1, sticky=W, pady=__class__.pady_val)

        self.lbl_rush = Label(self, bg=bg_color, font=self.__class__.label_font, text=self.__class__.lbl_rush_text)
        self.lbl_rush.grid(row=5, column=0, rowspan=2, sticky=W, ipady=__class__.pady_val)
        self.entry_note_priority = Entry(self, width=6, bg=bg_color, borderwidth=0, font=self.__class__.data_font, text=self.prrt_ctrlvar)
        self.entry_note_priority.bind('<Tab>', self.action_priority2bgcolor)  # may be will change back from '<Tab>' to '<Return>'
        self.entry_note_priority.grid(row=5, column=1, sticky=W, pady=__class__.pady_val)

    def action_remove_note(self, event):
        """This method deletes the note;
        activated by click on button Remove('X') of the specific note"""
        if messagebox.askyesno('Delete', 'Are you sure?', default='no'):
            del notes_dict[self.note_dbid]  # deleting note entry from the notes dictionary
            aux_filter_notes(category_filter_ctrlvar.get(), descr_filter_ctrlvar.get())

            clean_display()  # cleaning the display
            display_notes() # new display - does not contain frame of the deleted note

            db_delete_note(self.note_dbid) # deleting note record from the DB

    def action_update_note(self, event):
        """This method updates the note;
        activated by click on button Confirm Update('V') of the specific note frame"""
        self.action_fix_category()
        self.action_priority2bgcolor()

        # collecting details of the displayed note from the control variables
        n_ctgr = self.ctgr_ctrlvar.get().strip()
        n_descr = self.text_note_descr.get(1.0, '1.end').strip()
        n_date = self.date_ctrlvar.get().strip()
        n_priority = self.prrt_ctrlvar.get().strip()

        # overriding value of the note record wuth updated value (TBD note_dbid - proper getter?)
        updated_note_obj = NotePureData(n_ctgr, n_descr, n_date, n_priority, self.note_dbid)
        notes_dict[self.note_dbid] = updated_note_obj
        messagebox.showinfo('Update', 'done')

        aux_filter_notes(category_filter_ctrlvar.get(), descr_filter_ctrlvar.get())
        display_notes() # new display - contains details of the updated note (if still meets filtering criteria)
        db_update_note(updated_note_obj) # updating note record in the DB

    def action_fix_category(self, event=None):
        """This method changes category name typed by the user to capitalized"""
        category = self.ctgr_ctrlvar.get().strip()  # reading displayed category value

        # changing value inseted by the user to capitalized: 'Personal' / 'Work' / 'College' / 'Home'
        category = category.capitalize()

        # in case invalid category name has been inserted by the user, changing to default value 'Personal'
        if category not in category_names_lst:
            category = category_names_lst[0]

        self.ctgr_ctrlvar.set(category)  # fixed category value is immediately reflected in UI

    def fix_priority(self):
        """This method changes priority name typed by the user to capitalized
        Auxiliary function - called by method action_priority2bgcolor"""
        # reading displayed priority value
        priority = self.prrt_ctrlvar.get().strip()

        # changing value inseted by the user to capitalized: 'Low' / 'High' / 'Normal'
        priority = priority.capitalize()

        # in case invalid priority name has been inserted by user, changing to default value 'Normal'
        if priority not in priority_names_lst:
            priority = priority_names_lst[1]

        return priority

    def action_priority2bgcolor(self, event=None):
        """This method sets background color of the frame according to the currently defined priority
        Activated by hitting the Tab keyboard key"""
        priority = self.fix_priority()  # changing priority value to capitalized
        self.prrt_ctrlvar.set(priority)  # fixed priority value is immediately reflected in UI

        # setting value of background color according to priority
        bgcolor = prrt2color_dict[priority]  # {'Low':'lightgreen', 'Normal':'lightyellow', 'High':'lightpink'}

        # setting background color of the NoteView frame and all its widgets
        self.configure(bg=bgcolor)
        widgets_lst = [w for w in self.winfo_children() if isinstance(w, Label) or isinstance(w, Button) or isinstance(w, Entry) or isinstance(w, Text)]
        for w in widgets_lst:
            w.configure(bg=bgcolor)


class MainWindow(Frame):
    """This class defines UI and functionality of the application main window
    Derives from class Frame"""

    # class variables
    left_panel_width = 300
    left_upper_height = 270  # width required to display the calendar (date picker)
    notes_ctrl_height = 50
    base_color = 'bisque'
    cover_color = 'indianred'
    lbl_font = '"Century Gothic" 16'
    lbl_fontcolor = 'floralwhite'
    input_font = '"Segoe UI" 16'
    input_fontcolor = 'brown'
    btn_font = '"Century Gothic" 12 bold'
    btn_fontcolor = 'brown'
    str_by_category = 'filter by category:'
    str_by_text = 'filter by text:'
    str_newnote = 'newnote'
    noteview_side = 250
    note_padding = 5

    def __init__(self, container):
        """ctor"""
        super().__init__(container)
        container.update_idletasks()
        self.total_height = container.winfo_height()
        self.total_width = container.winfo_width()
        self.left_middle_height = self.left_lower_height = (self.total_height - __class__.left_upper_height) // 2
        self.right_area_width = self.total_width - __class__.left_panel_width
        self.notes_display_height = self.total_height - self.__class__.notes_ctrl_height

        self.msgboard_img = PhotoImage(file=msgboard_img_path)  # object that represents the background as cork-board texture
        self.justdoit_img = PhotoImage(file=justdoit_img_path)  # placeholder #1
        self.colornotes_img = PhotoImage(file=colornotes_img_path)  # placeholder #2

        self.create_widgets(container)

        # initial calculation of the grid dimensions according to the available space and the note frame size
        self.cnvs_notes_display.gridcols_cnt = self.right_area_width // (__class__.noteview_side + __class__.note_padding)
        self.cnvs_notes_display.gridrows_cnt = self.notes_display_height // (__class__.noteview_side + __class__.note_padding)
        self.cnvs_notes_display.grid_propagate(False)

    def create_widgets(self, container):
        """This method defines UI of the main window"""
        self.frm_main = Frame(container)
        self.frm_main.pack(fill=BOTH, expand=True)

        self.frm_left_main = Frame(self.frm_main, width=__class__.left_panel_width, height=self.total_height, bg=__class__.base_color)
        self.frm_left_main.pack(side=LEFT)

        self.frm_left_top = Frame(self.frm_left_main, width=__class__.left_panel_width, height=__class__.left_upper_height, bg=__class__.cover_color)
        self.frm_left_top.grid(row=0)
        self.frm_left_top.grid_propagate(False)
        self.calendar = Calendar(self.frm_left_top, padx_param=__class__.left_panel_width / 5, pady_param=__class__.left_upper_height / 8)

        self.frm_left_middle = Frame(self.frm_left_main, width=__class__.left_panel_width, height=self.left_middle_height, bg=__class__.base_color)
        self.frm_left_middle.grid(row=1)
        self.cnvs_left_middle = Canvas(self.frm_left_middle, width=self.left_panel_width, height=self.left_middle_height)  #, bg='white'
        self.cnvs_left_middle.grid(row=0, column=0)
        self.cnvs_left_middle.create_image(self.left_panel_width // 2, self.left_middle_height // 2, image=self.justdoit_img)

        self.frm_left_btm = Frame(self.frm_left_main, width=__class__.left_panel_width, height=self.left_lower_height, bg=__class__.base_color)
        self.frm_left_btm.grid(row=2)
        self.cnvs_left_bottom = Canvas(self.frm_left_btm, width=self.left_panel_width, height=self.left_lower_height)  #, bg='white'
        self.cnvs_left_bottom.grid(row=0, column=0)
        self.cnvs_left_bottom.create_image(self.left_panel_width // 2, self.left_lower_height // 2, image=self.colornotes_img)

        self.frm_right_main = Frame(self.frm_main, width=self.right_area_width, height=self.total_height, bg=__class__.base_color)
        self.frm_right_main.pack()

        self.frm_notes_control = Frame(self.frm_right_main, width=self.right_area_width, height=__class__.notes_ctrl_height, bg=__class__.cover_color)
        self.frm_notes_control.pack(fill=X)
        self.frm_notes_control.pack_propagate(False)

        self.lbl_filter_by_category = Label(self.frm_notes_control, font=__class__.lbl_font, fg=__class__.lbl_fontcolor, bg=__class__.cover_color, text=__class__.str_by_category)
        self.lbl_filter_by_category.pack(side=LEFT)

        self.cmbx_filter_by_category = Combobox(self.frm_notes_control, font=__class__.input_font, foreground=__class__.input_fontcolor, textvariable=category_filter_ctrlvar)  # ttk.Combobox
        self.cmbx_filter_by_category.configure(values=['All']+ category_names_lst)
        self.cmbx_filter_by_category.current(0)  # i.e. default value is 'All'
        self.cmbx_filter_by_category.bind("<<ComboboxSelected>>", self.action_filter_notes)
        self.cmbx_filter_by_category.pack(side=LEFT)

        self.lbl_filter_by_text = Label(self.frm_notes_control, font=__class__.lbl_font, fg=__class__.lbl_fontcolor, bg=__class__.cover_color, text=__class__.str_by_text)
        self.lbl_filter_by_text.pack(side=LEFT)

        self.entry_filter_by_text = Entry(self.frm_notes_control, font=__class__.input_font, fg=__class__.input_fontcolor, textvariable=descr_filter_ctrlvar)
        self.entry_filter_by_text.bind('<KeyRelease>', self.action_filter_notes)
        self.entry_filter_by_text.pack(side=LEFT)

        self.btn_new_note = Button(self.frm_notes_control, font=__class__.btn_font, fg=__class__.btn_fontcolor, text=__class__.str_newnote)
        self.btn_new_note.bind("<Button-1>", action_new_note_dialog)
        self.btn_new_note.pack(side=RIGHT, padx=5)

        self.frm_notes_display = Frame(self.frm_right_main, width=self.right_area_width, height=self.notes_display_height, bg='bisque')
        self.frm_notes_display.pack()

        self.cnvs_notes_display = Canvas(self.frm_notes_display, width=self.right_area_width, height=self.notes_display_height)
        self.cnvs_notes_display.bind('<Configure>', self.action_config_display)
        self.cnvs_notes_display.pack(fill=BOTH)
        self.cnvs_notes_display.create_image(self.right_area_width // 2, self.notes_display_height // 2, image=self.msgboard_img)

        self.sizegrip = Sizegrip(self)  #ttk.Sizegrip
        self.sizegrip.pack(side=RIGHT)

    def action_config_display(self, event):
        """This method deploys according to the new screen dimensions"""
        #self.after(250, clean_display())

        root.update_idletasks()
        self.total_height = root.winfo_height()
        self.total_width = root.winfo_width()
        self.left_middle_height = self.left_lower_height = (self.total_height - __class__.left_upper_height) // 2
        self.right_area_width = self.total_width - __class__.left_panel_width
        self.notes_display_height = self.total_height - self.__class__.notes_ctrl_height

        # recalculation of the grid dimensions according to available space and note frame size
        self.cnvs_notes_display.gridcols_cnt = self.right_area_width // (__class__.noteview_side + __class__.note_padding)
        self.cnvs_notes_display.gridrows_cnt = self.notes_display_height // (__class__.noteview_side + __class__.note_padding)

        self.action_filter_notes(event)

    def action_filter_notes(self, event=None):
        """This method displays notes that meet currentl filtering criteria"""

        aux_filter_notes(category_filter_ctrlvar.get(), descr_filter_ctrlvar.get())
        display_notes(event)


# main
# DB initialization
init()

root = Tk()
root.title('ToDoList')
root.state('zoomed')

#win_width, win_height = root.winfo_screenwidth() - 50, root.winfo_screenheight() - 90  # (//2) TBD: to decide regarding the initial size
win_width, win_height = root.winfo_width(), root.winfo_height()
root.geometry(f'{win_width}x{win_height}')
#root.geometry(f'{win_width}x{win_height}+10+10')
root.minsize(555, 320) ####

descr_filter_ctrlvar = StringVar()
category_filter_ctrlvar = StringVar()

frm_root = MainWindow(root)
root.mainloop()

# DB - termination of connection
terminate()
