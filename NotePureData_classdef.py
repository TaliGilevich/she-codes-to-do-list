class NotePureData:
    """This class represents note as a set of the following details: id, category, description, date, priority"""

    # class variable max_id is initialized in outer code right after uploading DB contents
    def __init__(self, category, description, date, priority, id=None):
        """ctor"""

        if id:  # existing note (either being uploaded from the DB or being updated), in this case id number is provided
            self.id = id # uniquely identifies the note, PK in the database
        else:  # new note: id number is to be generated
            self.__class__.max_id += 1
            self.id = self.__class__.max_id  # (also NotePureData.max_id)

        self.category = category
        self.description = description
        self.date = date
        self.priority = priority

    def __repr__(self):
        """ This method defines string representation of the note details"""
        return f'note id:\t\t{self.id}\ncategory:\t\t{self.category}\ndescription:\t{self.description}\ndate:\t\t\t{self.date}\npriority:\t\t{self.priority}\n'

    # TBD: getters / setters (__slots__) at least for db_id field