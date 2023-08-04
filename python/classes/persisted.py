from serializable import Serializable
from typing import Dict, List, Union, Optional

QueryObject = Dict
UpdateObject= Dict
CreateObject= Dict

InstanceOrQueryObject = Union["Persisted", QueryObject]
InstanceOrUpdateObject = Union["Persisted", UpdateObject]
InstanceOrCreateObject = Union["Persisted", CreateObject]

class Persisted(Serializable):
    _id_field_backend   = "_id"
    _id_serializer      = int
    _id_field_frontend  = "id"
    _id_deserializer    = str
    _query_object_type  = dict
    _update_object_type = dict
    _create_object_type = dict
    
    # ID related methods
    def get_id(self):
        return getattr(self, self._id_field_frontend)
    
    @classmethod
    def get_new_id(cls):
        raise NotImplementedError()
    
    @property
    def id_backend(self):
        return self.serialize_id()
    
    def serialize_id(self, id_ = None):
        return self._id_serializer(id_ or self.get_id())
    
    @classmethod
    def deserialize_id(cls, id_):
        return cls._id_deserializer(id_)
    
    
    # Functions to get objects for db calls
    def to_query_object(self, fields = None) -> QueryObject:
        if (
                not fields or
                fields == [self._id_field_frontend]
            ):
            return {
                self._id_field_backend: self.serialize_id()
            }
        backend_fields = list(map(self.field_maps_to, fields))
        return {
            k: v
            for k, v in self.serialize()
            if  k in backend_fields
        }

    def to_update_object(self) -> UpdateObject:
        return self.serialize()

    def to_create_object(self, force_id = False) -> CreateObject:
        d = self.serialize()
        if not force_id and self._id_field_backend in d.keys():
            raise KeyError(f"Id field {self._id_field_backend} manually set")
        d[self._id_field_backend] = self.get_new_id()
        return d
    
    @classmethod
    def cls_to_query_object(cls, o, **kwargs) -> QueryObject:
        if isinstance(o, cls._query_object_type):
            return o
        if isinstance(o, cls):
            return o.to_query_object(**kwargs)
        raise TypeError("Unhandled type of object")
    
    @classmethod
    def cls_to_update_object(cls, o, **kwargs) -> UpdateObject:
        if isinstance(o, cls._update_object_type):
            return o
        if isinstance(o, cls):
            return o.to_update_object(**kwargs)
        raise TypeError("Unhandled type of object")
    
    @classmethod
    def cls_to_create_object(cls, o, **kwargs) -> CreateObject:
        if isinstance(o, cls._create_object_type):
            return o
        if isinstance(o, cls):
            return o.to_create_object(**kwargs)
        raise TypeError("Unhandled type of object")

    # Quick instance methods / aliases
    def save(self, **kwargs):
        return self.upsert_one(
            self.to_query_object(), 
            self.to_update_object(),
            **kwargs
        )
    
    def reload(self, **kwargs):
        return self.load_one(
            self.to_query_object(), 
            **kwargs
        )


    # CRUD Ops
    @classmethod
    def load_one(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        query = cls.cls_to_query_object(query)
        raise NotImplementedError()
        # implement
        # result = None
        # if result is None:
        #     return None
        # return cls.deserialize(result)
    
    @classmethod
    def load_many(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> List["Persisted"]:
        query = cls.cls_to_query_object(query)
        raise NotImplementedError()
        # implement
        # results = []
        # if not len(results):
        #     return []
        # return list(map(cls.deserialize, results))
    
    @classmethod
    def create_one(cls, 
            create: InstanceOrCreateObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        create = cls.cls_to_create_object(query)
        raise NotImplementedError()
        # implement
        # result = None
        # if result is None:
        #     return None
        # return cls.deserialize(result)
        
    @classmethod
    def create_many(cls, 
            creates: List[InstanceOrCreateObject], 
            **kwargs
        ) -> List["Persisted"]:
        creates = list(map(cls.cls_to_create_object, creates))
        raise NotImplementedError()
        # implement
        # results = []
        # if not len(results):
        #     return []
        # return list(map(cls.deserialize, results))
        
    @classmethod
    def delete_one(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> bool:
        query = cls.cls_to_query_object(query)
        raise NotImplementedError()
        # implement
        # result = False
        # return result
        
    @classmethod
    def delete_many(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> int:
        query = cls.cls_to_query_object(query)
        raise NotImplementedError()
        # implement
        # result = 0
        # return result
        
    @classmethod
    def update_one(cls, 
            query: InstanceOrQueryObject, 
            update: InstanceOrUpdateObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        query = cls.cls_to_query_object(query)
        update= cls.cls_to_update_object(update)
        raise NotImplementedError()
        # implement
        # result = None
        # if result is None:
        #     return None
        # return cls.deserialize(result)
        
    @classmethod
    def update_many(cls, 
            query: InstanceOrQueryObject, 
            update: InstanceOrUpdateObject, 
            **kwargs
        ) -> List["Persisted"]:
        query = cls.cls_to_query_object(query)
        update= cls.cls_to_update_object(update)
        raise NotImplementedError()
        # implement
        # results = []
        # if not len(results):
        #     return []
        # return list(map(cls.deserialize, results))
        
    @classmethod
    def upsert_one(cls, 
            query: InstanceOrQueryObject, 
            update: InstanceOrUpdateObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        query = cls.cls_to_query_object(query)
        update = cls.cls_to_update_object(update)
        raise NotImplementedError()
        # implement
        # result = None
        # if result is None:
        #     return None
        # return cls.deserialize(result)
        
    @classmethod
    def upsert_many(cls, 
            queries: List[InstanceOrQueryObject], 
            updates: List[InstanceOrUpdateObject], 
            **kwargs
        ) -> List["Persisted"]:
        queries = list(map(cls.cls_to_query_object, queries))
        updates = list(map(cls.cls_to_update_object, updates))
        raise NotImplementedError()
        # implement
        # results = []
        # if not len(results):
        #     return []
        # return list(map(cls.deserialize, results))
