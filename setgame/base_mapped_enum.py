from aenum import IntEnum

class BaseMappedEnum(IntEnum):
    '''
    Extended IntEnum that allows further mapping to and from strings
    
    As in the parent IntEnum, define enum symbols (and only enum symbols) as static members.'''

    @staticmethod
    def get_format_mappings():
        '''
        Return a dict where keys are the enum symbols and values are their string representations.

        We use this method instead of a static member since IntEnum requires all static members to be ints.'''

        raise NotImplementedError()

    @classmethod
    def format(cls, s):
        return cls.get_format_mappings()[s]

    @classmethod
    def from_str(cls, s):
        format_mappings = cls.get_format_mappings()
        mappings_by_string = {v: k for k, v in format_mappings.iteritems()}
        return mappings_by_string[s]