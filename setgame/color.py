from aenum import IntEnum

class SetColor(IntEnum):
    red = 0
    green = 1
    purple = 2

    @staticmethod
    def format(s):
        formats = {
            SetColor.red: 'red',
            SetColor.green: 'green',
            SetColor.purple: 'purple'
        }

        return formats[s]
