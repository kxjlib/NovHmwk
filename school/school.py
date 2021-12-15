"""
School Class
Holds information about the school, and the people within.
"""


class School():
    _school_ids_used = []

    def __init__(self, people:list = []):
        self.people = []
        self.school_id = len(School._school_ids_used) +1
        School._school_ids_used.append(self.school_id)

    """
    Get All
    From the self.people list, return all people that are type
    """

    def get_all(self, person_type) -> list:
        return [_ for _ in self.students if isinstance(_, person_type)]

