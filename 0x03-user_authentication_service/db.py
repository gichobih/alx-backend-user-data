#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class for managing the database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new User instance and save it to the database.
        
        Args:
            email: User's email address.
            hashed_password: User's hashed password.
        
        Returns:
            The created User object.
        """
        session = self._session()
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
            return new_user
        except Exception as e:
            session.rollback()
            print(f"Error adding user: {e}")
            return None

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given attributes.
        
        Args:
            kwargs: Dictionary of attributes to use as search parameters.
        
        Returns:
            The User object matching the query.
        
        Raises:
            InvalidRequestError: If an invalid attribute is provided.
            NoResultFound: If no matching user is found.
        """
        session = self._session()
        query = session.query(User).filter_by(**kwargs).first()
        if query is None:
            raise NoResultFound("No user found with the specified attributes.")
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update attributes of a user.
        
        Args:
            user_id: The ID of the user to update.
            kwargs: Attributes to update with their new values.
        
        Raises:
            ValueError: If an invalid attribute is provided.
        """
        session = self._session()
        user = self.find_user_by(id=user_id)
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise ValueError(f"Invalid attribute: {attr}")
            setattr(user, attr, val)
        session.commit()
