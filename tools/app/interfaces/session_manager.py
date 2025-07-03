#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Protocol, Optional

from sqlalchemy.orm import Session


class ISessionManager(Protocol):
    """
    Протокол для менеджера сессий БД.
    
    Определяет интерфейс для работы с сессиями SQLAlchemy.
    Соответствует интерфейсу SessionManager.
    """

    def get_session(self, session_id: Optional[str] = None) -> Session:
        """
        Получает сессию БД.

        Args:
            session_id (Optional[str]): Идентификатор сессии.
                Если None, возвращает дефолтную сессию.

        Returns:
            Session: Сессия БД
        """
        ...

    def close_session(self, session_id: Optional[str] = None) -> None:
        """
        Закрывает сессию БД.

        Args:
            session_id (Optional[str]): Идентификатор сессии.
                Если None, закрывает дефолтную сессию.
        """
        ...
