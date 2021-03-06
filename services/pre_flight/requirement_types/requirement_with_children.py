from .requirement_type import Requirement


class RequirementWithChildren(Requirement):

    def __init__(self, name):
        super(RequirementWithChildren, self).__init__(name)
        self.__child_list = []

    def add_child(self, child):
        self.__child_list.append(child)

    def get_children(self):
        return self.__child_list
