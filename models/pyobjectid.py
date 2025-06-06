from pydantic_core import core_schema
from bson import ObjectId
from typing import Annotated, Any, ClassVar


class PyObjectId(str):
    """Custom type for handling MongoDB ObjectId fields with Pydantic v2"""
    
    @classmethod
    def __get_validators__(cls):
        # For backward compatibility with Pydantic v1 (not needed in v2)
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        # For backward compatibility with Pydantic v1 (not needed in v2)
        if not isinstance(v, ObjectId):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            v = ObjectId(v)
        return str(v)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        """
        Method for Pydantic v2 schema generation
        """
        return core_schema.chain_schema([
            # First check if it's a string and validate
            core_schema.str_schema(),
            # Then convert and validate with our custom validator
            core_schema.no_info_plain_validator_function(cls.validate)
        ])