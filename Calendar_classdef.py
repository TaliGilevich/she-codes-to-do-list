from datetime import date, MAXYEAR, MINYEAR
from calendar import month_name
from tkinter import Frame, Label, Button, StringVar, DISABLED, NORMAL
from MonthDispatcher_classdef import MonthDispatcher

class Calendar(Frame):
    """This class represents a date-picker.
    Inherits from the Tkinter Frame Class.
    Object of this class is designed either to work independently or to serve as date-picker component within DateTimePicker.
    Responsible for providing framework for date selection operations including following:
     - navigation between months either via UI(navigation buttons) or via keyboard(arrow-left and arrow-right keys)
     - displaying calendar of the month currently navigated to
     - making possible selection of date
     TBD: storing and providing up-to-date information regarding the selected date.
    """
    # class variables
    today_date = date.today()  # WILL BE NECESSARY TO UPDATE WHEN COMPUTER DATE CHANGES AT MIDNIGHT   #datetime.date.today()
    month_names_lst = list(month_name) #calendar.month_name

    bgcolor = 'snow2'
    month_year_font = '"Tempus Sans ITC" 10'
    shiftbtn_font = 'Arial 8 bold'
    shift_back_text = '<'  # '\u23EA'    # to watch here: https://unicode-search.net/unicode-namesearch.pl?term=ARROW
    shift_forward_text = '>'  # '\u23E9'

    def __init__(self, container, padx_param=0, pady_param=0):
        """ctor"""

        super().__init__(container)

        # control variable for 'MonthName yyyy' value
        self.month_year_ctrlvar = StringVar()
        self.month_year_ctrlvar.set(__class__.today_date.strftime("%B %Y"))  # initial value is 'CurrentMonth CurrentYear' e.g.'July 2019'

        self.create_widgets(container, padx_param, pady_param)
        self.lbl_month_year.focus_set()  ###

        # enabling navigation between months using arrow-left and arrow-right keys
        self.shiftback_funcid = self.lbl_month_year.bind('<Left>', self.action_shift_month_back)
        self.shiftfwd_funcid = self.lbl_month_year.bind('<Right>', self.action_shift_month_forward)

        # initialization - displaying calendar of the current month of the year
        self.month_dispatcher = MonthDispatcher(self.frm_display, __class__.today_date.year, __class__.today_date.month)

    def create_widgets(self, container, padx_val, pady_val):
        """This method defines UI of the date picker"""
        self.frm_main_calendar = Frame(container)
        self.frm_main_calendar.grid(row=0, ipady=5, padx=padx_val, pady=pady_val)
        #self.frm_main_calendar.grid_propagate(False)

        self.frm_month_year = Frame(self.frm_main_calendar, bg=__class__.bgcolor)
        self.frm_month_year.grid(row=0, padx=10, pady=10)

        self.btn_shift_back = Button(self.frm_month_year, command=self.action_shift_month_back, width=1, text=__class__.shift_back_text, font=__class__.shiftbtn_font, bd=0, bg=__class__.bgcolor)
        self.btn_shift_back.grid(row=0, column=0)

        self.lbl_month_year = Label(self.frm_month_year, width=17, textvariable=self.month_year_ctrlvar, font=__class__.month_year_font, bg=__class__.bgcolor)
        self.lbl_month_year.grid(row=0, column=1)

        self.btn_shift_forward = Button(self.frm_month_year, command=self.action_shift_month_forward, width=1, text=__class__.shift_forward_text, font=__class__.shiftbtn_font,bd=0, bg=__class__.bgcolor)
        self.btn_shift_forward.grid(row=0, column=2)

        self.frm_display = Frame(self.frm_main_calendar)  # place holder for calendar of the month navigated to
        self.frm_display.grid(row=1, padx=10)

    def action_shift_month_back(self, event=None):  # event=None, day_to_select=None: for the future use
        """This method is a callback for mouse click on shift-month-back button / for hitting arrow-left keyboard key
        It is responsible for performing navigation to preceding month including following:
        - calculation and displaying values of the target month and year
        - making decision whether to block further navigation back
        - invoking generation of the target month calendar
        """
        # enabling navigation forward because moving one step back ensures it is possible to go at least one step forward
        self.btn_shift_forward.configure(state=NORMAL)  # enabling the shift-month-forward button
        self.shiftfwd_funcid = self.lbl_month_year.bind('<Right>', self.action_shift_month_forward)  # binding a callback for the arrow-right keyboard key

        # retrieving values of the currently displayed month and year
        displayed_month, displayed_year = self.month_year_ctrlvar.get().split(' ')
        displayed_year = int(displayed_year)
        month_index = __class__.month_names_lst.index(displayed_month)

        # calculation of the target month and year; in case minimum valid month is reached, blocking further navigation back
        month_index -= 1
        if displayed_year == MINYEAR and month_index == date.min.month:  # year:1, month: 1 (January)  #datetime.MINYEAR  datetime.date.min.month
            self.btn_shift_back.configure(state=DISABLED)  # disabling the shift-month-back button
            self.lbl_month_year.unbind('<Left>', self.shiftback_funcid)  # unbinding a callback for the arrow-left keyboard key
        elif month_index == 0:
            month_index = 12
            displayed_year -= 1

        # updating control variable that stores <MonthName yyyy> value - new value being immediately reflected in UI
        self.month_year_ctrlvar.set(f'{__class__.month_names_lst[month_index]} {displayed_year}')

        # creating calendar of the target month
        self.month_dispatcher.arrange_month(displayed_year, month_index)

    def action_shift_month_forward(self, event=None):  # event=None, day_to_select=None: for future use
        """This method is a callback for mouse click on shift-month-forward button / for hitting arrow-right keyboard key
         It is responsible for performing navigation to succeeding month including following:
         - calculation and displaying values of the target month and year
         - making decision whether to block further navigation forward
         - invoking generation of the target month calendar
         """
        # enabling navigation back because moving one step forward ensures it is possible to go at least one step back
        self.btn_shift_back.configure(state=NORMAL)  # enabling the shift-month-back button
        self.shiftback_funcid = self.lbl_month_year.bind('<Left>', self.action_shift_month_back)  # binding a callback for the arrow-left keyboard key

        # retrieving values of the currently displayed month and year
        displayed_month, displayed_year = self.month_year_ctrlvar.get().split(' ')
        displayed_year = int(displayed_year)
        month_index = __class__.month_names_lst.index(displayed_month)

        # calculation of the target month and year; in case maximum valid month is reached, blocking further navigation forward
        month_index += 1
        if displayed_year == MAXYEAR and month_index == date.max.month:  # year:9999, month: 12 (December)   #datetime.MAXYEAR  datetime.date.max.month
            self.btn_shift_forward.configure(state=DISABLED)  # disabling the shift-month-forward button
            self.lbl_month_year.unbind('<Right>', self.shiftfwd_funcid)  # unbinding a callback for the arrow-right keyboard key
        elif month_index == 13:
            month_index = 1
            displayed_year += 1

        # updating control variable that stores <MonthName yyyy> value - new value being immediately reflected in UI
        self.month_year_ctrlvar.set(f'{__class__.month_names_lst[month_index]} {displayed_year}')

        # creating calendar of the target month
        self.month_dispatcher.arrange_month(displayed_year, month_index)