import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, BigInteger,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True, index=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    language_code = Column(String(10), nullable=True)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    registration_date = Column(DateTime, default=datetime.datetime.utcnow)

    interests = Column(ARRAY(String), nullable=True)
    subscription_status = Column(String, default="free")

    subscribed_channels = Column(ARRAY(BigInteger), default=list, nullable=True)
    managed_channels = Column(ARRAY(BigInteger), default=list, nullable=True)

    free_views = Column(Integer, default=1000)

    referrer_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=True)
    referrals_count = Column(Integer, default=0)

    referral_bonus_views = Column(Integer, default=0)

    activities = relationship("UserActivity", back_populates="user")
    user_state = relationship("UserState", uselist=False, back_populates="user")

    premium = relationship("PremiumUser", uselist=False, back_populates="user", lazy="joined")  # 🔧 исправлено

    @property
    def premium_views(self):
        return self.premium.premium_views if self.premium else 0

    @property
    def referral_views(self):
        return self.premium.referral_bonus_views if self.premium else 0

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username})>"

class Channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(BigInteger, primary_key=True, unique=True, index=True)
    channel_name = Column(String(100), nullable=False)
    channel_link = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    member_count = Column(Integer, nullable=True)
    additional_info = Column(String(255), nullable=True)

    posts_count = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)

    monthly_limit = Column(Integer, default=1000)
    monthly_views_left = Column(Integer, default=1000)

    admin_user_ids = Column(ARRAY(BigInteger), default=list)

    def __repr__(self):
        return f"<Channel(channel_id={self.channel_id}, channel_name={self.channel_name})>"

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = (UniqueConstraint('channel_id', 'message_id', name='uix_channel_message'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger, nullable=False)
    message_id = Column(Integer, nullable=False)
    interests = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    channel_name = Column(Text, nullable=True)

    views_count = Column(Integer, default=0)
    reactions_count = Column(Integer, default=0)
    clicks_count = Column(Integer, default=0)

    reactions_count_heart = Column(Integer, default=0)
    reactions_count_like = Column(Integer, default=0)
    reactions_count_dislike = Column(Integer, default=0)

    activities = relationship("UserActivity", back_populates="post")

    def __repr__(self):
        return f"<Post(id={self.id}, channel_id={self.channel_id}, message_id={self.message_id})>"

class UserActivity(Base):
    __tablename__ = 'user_activity'

    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    action_type = Column(String(50), nullable=False)
    action_timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="activities")
    post = relationship("Post", back_populates="activities")

class Interest(Base):
    __tablename__ = 'interests'

    interest_id = Column(Integer, primary_key=True, autoincrement=True)
    interest_name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Interest(interest_id={self.interest_id}, interest_name={self.interest_name})>"

class UserState(Base):
    __tablename__ = 'user_state'

    user_id = Column(BigInteger, ForeignKey('users.user_id'), primary_key=True)
    last_read_post_id = Column(Integer, default=0)
    unread_posts_count = Column(Integer, default=0)

    user = relationship("User", back_populates="user_state")

    def __repr__(self):
        return f"<UserState(user_id={self.user_id}, last_read_post_id={self.last_read_post_id}, unread_posts_count={self.unread_posts_count})>"

class PremiumUser(Base):
    __tablename__ = 'premium_users'

    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    premium_views = Column(Integer, default=0)
    referral_bonus_views = Column(Integer, default=0)
    activated_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="premium")

    def __repr__(self):
        return f"<PremiumUser(user_id={self.user_id}, premium={self.premium_views}, referral={self.referral_bonus_views})>"
