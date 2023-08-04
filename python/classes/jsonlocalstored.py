from persisted import *

import json
import os
import time

class JSONLocalStored(Persisted):
    _db_path    = "local_storage.json"
    _collection = ""
    _db_exists  = None
    """
    This is just a basic test for the api / a way to not have to mess with
    dbs all the time. It saves things on the _db_path specified. It's just
    the antithesis of performance (reload / rewrite the entire json at each
    call) but its purpose is just to mimick a kind of sqlite version for nosql
    """
    @classmethod
    def _load_db_data(cls) -> Union[List, Dict]:
        if not cls._db_exists and not os.path.isfile(cls._db_path):
            cls._dump_db_data([] if not cls._collection else {})
        with open(cls._db_path, 'r', encoding='utf8') as fi:
            return json.load(fi)
    
    @classmethod
    def _dump_db_data(cls, data: Union[List, Dict]):
        with open(cls._db_path, 'w', encoding='utf') as fo:
            json.dump(data, fo)
    
    @classmethod
    def _load_data(cls) -> List:
        db_data = cls._load_db_data()
        wrapper = db_data
        subpaths = cls._collection.split(".")
        for i, key in enumerate(subpaths):
            if key == "":
                return wrapper
            if i == (len(subpaths) - 1):
                return wrapper.get(key)
            wrapper = wrapper.get(key, {})
        raise ValueError("db collection path seems wrong")
    
    @classmethod
    def _dump_data(cls, data: List[Dict]):
        db_data = cls._load_db_data()
        wrapper = db_data
        subpaths = cls._collection.split(".")
        for i, key in enumerate(subpaths):
            if key == "":
                return cls._dump_db_data(data)
            if i == (len(subpaths) - 1):
                wrapper.set(key, data)
                return cls._dump_db_data(db_data)
            if not key in wrapper.keys():
                wrapper[key] = {}
            wrapper = wrapper[key]
        raise ValueError("db collection path seems wrong")
    
    @staticmethod
    def _json_query_comparison(
            query: InstanceOrQueryObject, 
            other: Dict
        ):
        return all(
            query[k] == other[k]
            for k in query.keys()
        )
    
    @classmethod
    def _do_query(cls,
            query: InstanceOrQueryObject, 
            data: List[Dict]
        ) -> filter:
        return filter(lambda d: cls._json_query_comparison(query, d), data)

    @classmethod
    def get_new_id(cls) -> int:
        time.sleep(0.05)
        return int(time.time() * 1000)
    
    @classmethod
    def load_one(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        query = cls.cls_to_query_object(query)
        data = cls._load_data()
        try:
            result = next(cls._do_query(query, data))
        except StopIteration:
            return None
        return cls.deserialize(result)
    
    @classmethod
    def load_many(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> List["Persisted"]:
        query = cls.cls_to_query_object(query)
        data = cls._load_data()
        results = cls._do_query(query, data)
        return list(map(cls.deserialize, results))
    
    @classmethod
    def create_one(cls, 
            create: InstanceOrCreateObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        create = cls.cls_to_create_object(query)
        data = cls._load_data()
        data.append(create)
        cls._dump_data(data)
        return cls.deserialize(create)
        
    @classmethod
    def create_many(cls, 
            creates: List[InstanceOrCreateObject], 
            **kwargs
        ) -> List["Persisted"]:
        creates = list(map(cls.cls_to_create_object, creates))
        data = cls._load_data()
        data.extend(creates)
        cls._dump_data(data)
        return list(map(cls.deserialize, creates))
        
    @classmethod
    def delete_one(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> bool:
        query = cls.cls_to_query_object(query)
        data = cls._load_data()
        target = None
        for i, record in enumerate(data):
            if cls._json_query_comparison(query, record):
                target = i
                break
        if not target is None:
            data.pop(target)
            cls._dump_data(data)
            return True
        return False
        
    @classmethod
    def delete_many(cls, 
            query: InstanceOrQueryObject, 
            **kwargs
        ) -> int:
        query = cls.cls_to_query_object(query)
        data = cls._load_data()
        targets = []
        for i, record in enumerate(data):
            if cls._json_query_comparison(query, record):
                target.append(i)
        if lt:=len(targets):
            for target in reversed(targets):
                data.pop(target)
            cls._dump_data(data)
            return lt
        return 0
        
    @classmethod
    def update_one(cls, 
            query: InstanceOrQueryObject, 
            update: InstanceOrUpdateObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        query = cls.cls_to_query_object(query)
        update= cls.cls_to_update_object(update)
        data = cls._load_data()
        for record in data:
            if cls._json_query_comparison(query, record):
                record.update(update)
                cls._dump_data(data)
                return cls.deserialize(record)
        return None
        
    @classmethod
    def update_many(cls, 
            query: InstanceOrQueryObject, 
            update: InstanceOrUpdateObject, 
            **kwargs
        ) -> List["Persisted"]:
        query = cls.cls_to_query_object(query)
        update= cls.cls_to_update_object(update)
        data = cls._load_data()
        results = []
        for record in data:
            if cls._json_query_comparison(query, record):
                record.update(update)
                results.append(record)
        if len(results):
            cls._dump_data(data)
            return list(map(cls.deserialize, results))
        return []
        
    @classmethod
    def upsert_one(cls, 
            query: InstanceOrQueryObject, 
            update: InstanceOrUpdateObject, 
            **kwargs
        ) -> Optional["Persisted"]:
        query = cls.cls_to_query_object(query)
        update = cls.cls_to_update_object(update)
        data = cls._load_data()
        for record in data:
            if cls._json_query_comparison(query, record):
                record.update(update)
                cls._dump_data(data)
                return cls.deserialize(record)
        data.append(update)
        cls._dump_data(data)
        return cls.deserialize(update)
        
    @classmethod
    def upsert_many(cls, 
            queries: List[InstanceOrQueryObject], 
            creates: List[InstanceOrUpdateObject], 
            **kwargs
        ) -> List["Persisted"]:
        raise NotImplementedError()
