from base_mapped_enum import BaseMappedEnum

class SetColor(BaseMappedEnum):
    red = 0
    green = 1
    purple = 2

    @staticmethod
    def get_format_mappings():
        return {
            SetColor.red: 'red',
            SetColor.green: 'green',
            SetColor.purple: 'purple'
        }