
from bot.db.base import Base

from sqlalchemy import Column, BigInteger, Boolean, select


class Formatter(Base):
    __tablename__ = 'formatter'

    chat_id = Column(BigInteger, unique=True, primary_key=True)
    auto_format = Column(Boolean, default=True)
    auto_delete = Column(Boolean, default=True)

    @classmethod
    async def find(self, db_session, chat_id):
        sql = select(self).where(self.chat_id == chat_id)
        result = await db_session.execute(sql)
        return result.scalars().first()

    def __str__(self) -> str:
        return f'<Formatter:{self.chat_id}>'
