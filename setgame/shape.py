from aenum import IntEnum

class SetShape(IntEnum):
    diamond = 0
    squiggles = 1
    oval = 2

    @staticmethod
    def format(s):
        formats = {
            SetShape.diamond: 'diamond',
            SetShape.squiggles: 'squiggle',
            SetShape.oval: 'oval'
        }

        return formats[s]
