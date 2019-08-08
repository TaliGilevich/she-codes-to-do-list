from tkinter import Button

class DayKey(Button):
    """This class is responsible for representing a day as it appears in the month calendar.
    Inherits from the Tkinter Button Class.
    Has specific characteristics as follows:
    - Text value that represents a day component of the datetime object
    - Flags that determine whether given day is today and/or belongs to displayed month and/or selected
    These flags affect appearance of each DayKey widget.

    TBD Mouse click on the widget of this class 'selects' the day and updates the day component of the date being picked.

    """
    # class variables
    font_name = 'Tahoma 8'
    regular_bgcolor = 'snow2'
    default_bgcolor = 'snow'#'linen' #'old lace'
    default_fgcolor = 'black'
    #offmonth_bgcolor = 'snow'
    offmonth_fgcolor = 'grey'
    today_bgcolor = 'misty rose2'
    today_fgcolor = 'black'
    selected_bgcolor = 'indianred'
    selected_fgcolor = 'floralwhite'

    default_bdwidth = 0

    def __init__(self, parent_frame, textval, offmonth_flag=False, today_flag=False, selected_flag=False):
        """ctor"""
        self.is_off_month = offmonth_flag
        self.is_today = today_flag
        self.is_selected = selected_flag

        super().__init__(parent_frame, bd=__class__.default_bdwidth, font=__class__.font_name, text=textval, width=2) #bg=__class__.default_bgcolor,
        self.design()
        self.bind('<Button-1>', self.action_report_selected_day)  # temporary - for debugging purposes

    def design(self):
        """This method is responsible for setting appearance of the DayKey widget according to its characteristics:
        regular day(default appearance) / today's day / off-month day i.e. day that belongs either to next or to previous month / currently selected day

        """
        bgcolor, fontcolor = __class__.default_bgcolor, __class__.default_fgcolor #offmonth
        if self.is_off_month:
            bgcolor, fontcolor = __class__.default_bgcolor, __class__.offmonth_fgcolor
        if self.is_today:
            bgcolor, fontcolor = __class__.today_bgcolor, __class__.today_fgcolor
        if self.is_selected:
            bgcolor, fontcolor = __class__.selected_bgcolor, __class__.selected_fgcolor

        self.configure(bg=bgcolor, fg=fontcolor)

    def action_report_selected_day(self, event):
        """This method is a callback for the leftmost mouse button press
        TBD following effects: deselecting previously selected day; making data of the currently selected day available to encapsulating classes (MonthDispatcher and/or Calendar)

        """
        selected_day = self.cget('text')
        print(f"date {selected_day}, belongs to the displayed month: {not self.is_off_month}, today's date: {self.is_today}")
        if self.is_off_month:
            if selected_day < 14:  # i.e. this date belongs to the succeeding month
                print('\tbelongs to the next month')  # TBD: navigation to succeeding month then setting required selection
            elif selected_day > 21:  # i.e. this date belongs to the preceding month
                print('\tbelongs to the preceding month')  # TBD: navigation to preceding month then setting required selection

        return selected_day  # temporary - POC

