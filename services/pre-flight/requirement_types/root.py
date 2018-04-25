from .requirement_with_children import RequirementWithChildren


class Root(RequirementWithChildren):

    def __init__(self, name):
        super(Root, self).__init__(name)
