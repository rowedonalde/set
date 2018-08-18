from base_mapped_enum import BaseMappedEnum

class SetShading(BaseMappedEnum):
    solid = 0
    empty = 1
    striped = 2

    @staticmethod
    def get_format_mappings():
        return {
            SetShading.solid: 'solid',
            SetShading.empty: 'empty',
            SetShading.striped: 'striped'
        }