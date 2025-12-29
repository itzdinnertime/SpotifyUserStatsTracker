from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type, List

T = TypeVar('T')

class BaseRepo(Generic[T]):
    
    def __init__ (self, session: Session, model: Type[T]):
        self.session = session
        self.model = model
        
    def add(self, entity: T) -> T:
        self.session.add(entity)
        self.session.flush()
        
        return entity
        
    def add_all(self, entities: List[T]) -> List[T]:
        self.session.add_all(entities)
        self.session.flush()
        
        return entities
        
    def get_by_id(self, id: int):
        return self.session.query(self.model).filter(self.model.id == id).first()
        
    def get_all(self):
        return self.session.query(self.model).all()
        
    def delete_by_user_id(self, user_id: int):
        count = self.session.query(self.model).filter(self.model.user_id == user_id).delete()
        
        return count
        
    def commit(self):
        self.session.commit()
