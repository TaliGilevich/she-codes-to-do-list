from tkinter import END
from CommonDefinitions import notes_views_lst, notes_dict, notes_to_display_lst
from DBOperations import db_select_notes, db_get_max_noteid, db_clean_tbl_notes, db_insert_note, db_init, db_terminate
from NotePureData_classdef import NotePureData

def clean_display():
    """This function cleans displayed notes"""

    for noteframe in notes_views_lst:
        noteframe.grid_forget()
    notes_views_lst.clear()

def aux_filter_notes(categ_filter_str, descr_filter_str):
    """This function determines notes that meet currently defined filtering criteria
    Auxiliary function, called by action_filter_notes
    Populates notes_to_display_lst with objects of type NotePureData
    """

    notes_to_display_lst.clear()
    notes_objects_lst = list(notes_dict.values())  # list of all existing notes (i.e. objects of type NotePureData)

    if descr_filter_str == '' and categ_filter_str == 'All':
        notes_to_display_lst.extend(notes_objects_lst[:])
    elif descr_filter_str != "" and categ_filter_str != 'All':
        notes_to_display_lst.extend(list(set([nobj for nobj in notes_objects_lst if nobj.category == categ_filter_str and nobj.description.find(descr_filter_str) != -1])))
    elif categ_filter_str != 'All':
        notes_to_display_lst.extend([nobj for nobj in notes_objects_lst if nobj.category == categ_filter_str])
    else:  # elif descr_filter_str != ''
        notes_to_display_lst.extend([nobj for nobj in notes_objects_lst if nobj.description.find(descr_filter_str) != -1])

def highlight_match(note_frame, text_to_find):
    """This function highlights substring in the Description field of the displayed note that matches current filtering criteria
    Auxiliary function - called by the general function display_notes
    """

    tag_name = 'highlight'
    highlight_color = "yellow"

    start_highlight = note_frame.text_note_descr.get(1.0, END).find(text_to_find)
    end_highlight = start_highlight + len(text_to_find)

    # TBD note_frame.text_note_descr - proper getter
    note_frame.text_note_descr.tag_add(tag_name, f'1.{start_highlight}', f'1.{end_highlight}')
    note_frame.text_note_descr.tag_config(tag_name, background=highlight_color)  # TBD: as above

    return note_frame

def download_from_db():
    """This function downloads data from the database notes table"""

    notes_db_records_lst = db_select_notes()
    if len(notes_db_records_lst) > 0:  # DB is not empty; stored records are to be downloaded
        NotePureData.max_id = db_get_max_noteid()
        for rcrd in notes_db_records_lst:
            notes_dict[rcrd[0]] = NotePureData(rcrd[1], rcrd[2], rcrd[3], rcrd[4], rcrd[0])
    else:  # DB is empty
        NotePureData.max_id = 0

def init():
    """This function is responsible for the DB initialization and for the downloading stored data on application startup"""

    db_init()
    download_from_db()

def upload_to_db():
    """This function uploads the data stored in the notes_objects_lst to the database notes table"""

    notes_objects_lst = list(notes_dict.values())
    db_clean_tbl_notes()
    for n in notes_objects_lst:
        db_insert_note(n)

def terminate():
    """This function is responsible for the uploading of existing data and for DB connection termination once application is closed"""

    upload_to_db()
    db_terminate()