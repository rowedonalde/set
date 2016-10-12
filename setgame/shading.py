from aenum import IntEnum

class SetShading(IntEnum):
    solid = 0
    empty = 1
    striped = 2

    @staticmethod
    def format(s):
        formats = {
            SetShading.solid: 'solid',
            SetShading.empty: 'empty',
            SetShading.striped: 'striped'
        }

        return formats[s]
