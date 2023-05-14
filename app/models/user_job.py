from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class UserJob(BareBaseModel):
    user_id = Column(ForeignKey('user.id'), primary_key=True)
    job_id = Column(ForeignKey('job.id'), primary_key=True)
    user = relationship("User", back_populates="jobs")
    job = relationship("Job", back_populates="users")
    ip = Column(String)
    imei = Column(String)

    # proxies
    # author_name = association_proxy(target_collection='author', attr='name')
    # book_title = association_proxy(target_collection='book', attr='title')
