post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)

    posts = relationship('Post', secondary=post_tags, back_populates='tags')

    def __repr__(self):
        return f"<Tag {self.name}>"
