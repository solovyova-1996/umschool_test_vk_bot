from sqlalchemy.orm import sessionmaker

from database.models import User


class UserOperations:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def create(self, vk_id: int, city: str):
        user = User(vk_id=vk_id, city=city)
        self.session.add(user)
        self.session.commit()
        return {"id": str(user.id), "vk_id": user.vk_id, "city": user.city}

    def get_user_by_vk_id(self, vk_id: int):
        user = self.session.query(User).filter_by(vk_id=vk_id).first()
        if user is not None:
            return {"id": str(user.id), "vk_id": user.vk_id, "city": user.city}
        else:
            return user

    def get_city_user_by_vk_id(self, vk_id: int):
        user = self.session.query(User).filter_by(vk_id=vk_id).first()
        if user is not None:
            return user.city
        else:
            return user

    def update_city(self, vk_id: int, new_city: str):
        user = self.session.query(User).filter_by(vk_id=vk_id).first()
        user.city = new_city
        self.session.commit()
        return user
