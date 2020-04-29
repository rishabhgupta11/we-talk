
# Related name is what the rel model would call this model
class Post(Model):
    timestamp = DateTimeField(default=datetime.now)
    user = ForeignKeyField(
        model=User,
        related_name='posts'
    )
    content = TextField()
    image = BlobField(null=True)
    imageThere = BooleanField(default=0)
    numLikes = IntegerField(default=0)
    numComments = IntegerField(default=0)

    def getLikes(self):
        """returns list of users who liked the post"""
        return (
            Post.select().join(
                Likes, on=Likes.post_id
            ).where(
                Likes.post_id == self
            )
        )

    class Meta:
        database = DATABASE_proxy
        order_by = ('-timestamp',)


class Relationship(Model):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')

    class Meta:
        database = DATABASE_proxy
        indexes = (
            ((('from_user', 'to_user'), True),)
        )


class Likes(Model):
    user_id = ForeignKeyField(User, related_name='user_likes', null=True)
    post_id = ForeignKeyField(Post, related_name='post_likes', null=True)

    class Meta:
        database = DATABASE_proxy


class Comments(Model):
    user_id = ForeignKeyField(User, related_name='user_likes', null=True)
    post_id = ForeignKeyField(Post, related_name='post_likes', null=True)
    comment = TextField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE_proxy


def initialize():
    DATABASE_proxy.connection()
    DATABASE_proxy.create_tables([User, Post, Relationship, Likes, Comments], safe=True)
    DATABASE_proxy.close()
