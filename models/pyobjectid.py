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
        This method is used by Pydantic v2 for schema creation.
        It defines how to convert and validate the ObjectId type.
        """
        return core_schema.union_schema([
            # Handle the case when we get an actual ObjectId
            core_schema.is_instance_schema(ObjectId, 
                core_schema.string_schema()),
            # Handle the case when we get a string representation
            core_schema.chain_schema([
                core_schema.string_schema(),
                core_schema.no_info_plain_validator_function(cls.validate)
            ])
        ])