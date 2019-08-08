category_names_lst = ['Personal', 'Work', 'College', 'Home']
priority_names_lst = ['Low', 'Normal', 'High']
priority_colors_lst = ['lightgreen', 'lightyellow', 'lightpink']

# generating priority-to-color dictionary in format priority:color e.g. {'Low':'lightgreen', 'Normal':'lightyellow', 'High':'lightpink'}
prrt2color_dict = dict(zip(priority_names_lst, priority_colors_lst))

notes_dict = {}  # dictionary of the notes' data (for each item, key is note ID, value is Note object) - logic level
notes_views_lst = []  # list of the NoteView objects - graphic representation of the notes
notes_to_display_lst = []  # list of the objects of type NotePureData that meet currently defined filtering criteria

msgboard_img_path = r'.\Images\cork_board.gif'  # path to the background file
justdoit_img_path = r'.\Images\just_do_it_.gif'  # path to the just-do-it picture file
colornotes_img_path = r'.\Images\color_notes_2.gif'  # path to the just-do-it picture file

# control variables that store currently defined filtering values
descr_filter_ctrlvar = object   # filter by description
category_filter_ctrlvar = object  # filter by category


