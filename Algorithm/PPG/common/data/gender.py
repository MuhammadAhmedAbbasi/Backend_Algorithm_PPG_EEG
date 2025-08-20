from enum import Enum

class Gender(Enum):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'N'

    @classmethod
    def from_str(cls, gender_str: str) -> 'Gender':
        try:
            return cls(gender_str)  
        except ValueError:
            raise ValueError(f"Invalid gender value: {gender_str}")