from base_mapped_enum import BaseMappedEnum

class SetShape(BaseMappedEnum):
    diamond = 0
    squiggles = 1
    oval = 2

    @staticmethod
    def get_format_mappings():
        return {
            SetShape.diamond: 'diamond',
            SetShape.squiggles: 'squiggle',
            SetShape.oval: 'oval'
        }