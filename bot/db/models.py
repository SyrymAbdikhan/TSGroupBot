
from bot.db.base import Base

from sqlalchemy import Column, BigInteger, Text, select


class ChatSettings(Base):
    __tablename__ = 'chat_settings'

    chat_id = Column(BigInteger, unique=True, primary_key=True)
    moodle_token = Column(Text)

    @classmethod
    async def find(self, db_session, chat_id):
        sql = select(self).where(self.chat_id == chat_id)
        result = await db_session.execute(sql)
        return result.scalars().first()

    def __str__(self) -> str:
        return f'<ChatSettings:{self.chat_id}>'
