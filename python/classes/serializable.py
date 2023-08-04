import json
from collections import OrderedDict
from typing import Dict, Callable, TypedDict, Any, Type, List, Union, Literal

# uncomment the following lines if you want to enable schema validation
# from marshmallow import Schema as MarshmallowSchema
SchemaType    = Any # MarshmallowSchema

# Typing
class SerializingMapping(TypedDict):
    key: Dict[str, Callable[[Any], Any]]
    cls: Dict[Type[Any], Callable[[Any], Any]]

NestedMapping = Dict[str, Union[Type["Serializable"], Literal["self"]]]

# Class Decorator (will make the class inherit from Serializable, if it's not)
def serializable(
        fields        : List[str]          = [],
        nested        : NestedMapping      = {},
        schema        : SchemaType         = None,
        serializers   : SerializingMapping = {}, 
        deserializers : SerializingMapping = {},
        json_encoder  : json.JSONEncoder   = None,
        json_decoder  : json.JSONDecoder   = None,
    ):
    """
    A decorator that makes a class inherit from Serializable if it's not already.
    It also sets up the serialization and deserialization methods for the class.
    """
    def wrapped(cls):
        if not issubclass(cls, Serializable):
            cls = type(cls.__name__, (cls, Serializable), {})
        
        cls._Serializable__json_encoder = json_encoder
        cls._Serializable__json_decoder = json_decoder
        
        if schema:
            if any([
                    fields,
                    nested,
                    serializers,
                    deserializers,
                    json_encoder,
                    json_decoder,
                ]):
                raise ValueError("Schema serialization cant be provided with " \
                                 "any of these params (fields, nested, serial" \
                                 "izers, deseri alizers")
            cls._Serializable__schema = schema
            return cls
            
        cls._Serializable__fields.extend(fields)
        
        cls._Serializable__nested.update({
            k: cls if v == "self" else v
            for k, v in nested.items()
        })
        
        for k in ["key", "cls"]:
            cls._Serializable__serializers[k].update(
                serializers.get(k, {})
            )
        for k in ["key", "cls"]:
            cls._Serializable__deserializers[k].update(
                deserializers.get(k, {})
            )

        return cls
    return wrapped


# Implementation
class Serializable:
    """
    The Serializable class provides methods for serializing and deserializing
    instances of the class. It can be inherited from directly, or a class can
    be made to inherit from it using the @serializable decorator.
    """
    __fields        : List[str]                         = []
    __nested        : NestedMapping                     = {}
    __schema        : SchemaType                        = None
    __serializers   : SerializingMapping                = {
        "key": {
            # "key": lambda o: o.__dict__,      # will serialize object at key 
            # "key" with its __dict__ property
            
            # high priority
        },
        "cls": {
            # dict : lambda o: list(o.items()), # will serialize all dicts as 
            # lists of k, v
            
            # medium priority
        },
    }
    __deserializers : SerializingMapping                = {
        "key": {
            # "key": lambda d: Serializable.deserialize(d), # will deserialize 
            # using a class method
            
            # high priority
        },
        "cls": {
            # float: lambda f: int(f) 
            
            # low priority
        }
    }
    __json_encoder  : json.JSONEncoder                  = None
    __json_decoder  : json.JSONDecoder                  = None

    def __serialize(self, field):
        v = getattr(self, field)
        if field in self._Serializable__nested.keys():
            return None if v is None else v._to_dict()
        strategy = (
            self._Serializable__serializers["key"].get(field) or 
            self._Serializable__serializers["cls"].get(v.__class__)
        )
        if not strategy is None:
            return strategy(v)
        return v
    
    @classmethod
    def __deserialize(cls, field, value):
        if c := cls._Serializable__nested.get(field):
            return None if None in [c, value] else c.deserialize(value)
        strategy = (
            cls._Serializable__deserializers["key"].get(field) or 
            cls._Serializable__deserializers["cls"].get(value.__class__)
        )
        if not strategy is None:
            return strategy(value)
        return value

    def _to_dict(self) -> dict:
        if schema := self._Serializable__schema:
            return schema.dump(self)
        return {
            field: self._Serializable__serialize(field)
            for field in self._Serializable__fields
        }

    @classmethod
    def _from_dict(cls, d: dict) -> dict:
        if schema := cls._Serializable__schema:
            return schema.load(d)
        return {
            field: cls._Serializable__deserialize(
                field,
                d[field]
            )
            for field in cls._Serializable__fields 
        }
    
    def _to_json(self) -> str:
        return json.dumps(
            self.to_dict(), 
            cls=self._Serializable__json_encoder
        )
    
    @classmethod
    def _from_json(self, s: str):
        return cls.from_dict(json.loads(
            s,
            cls=cls._Serializable__json_decoder
        ))
    
    def to_dict(self) -> dict:
        return self._to_dict()

    @classmethod
    def from_dict(cls, d: dict):
        kwargs = cls._from_dict(d)
        return cls(**kwargs)

    def to_json(self) -> str:
        return self._to_json()

    @classmethod
    def from_json(cls, s: str):
        return cls._from_json(s)

    def serialize(self) -> dict:
        return self.to_dict()

    @classmethod
    def deserialize(cls, d: dict):
        return cls.from_dict(d)
