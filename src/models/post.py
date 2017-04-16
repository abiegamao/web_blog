
from src.common.database import Database
import datetime, uuid

class Post(object): #this post comes from an object

    # Basic PROPERTIES of a POST
    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None): #default - only in the end
        self.blog_id = blog_id
        self.title =  title
        self.content = content
        self.author = author
        self._id = uuid.uuid4().hex if _id is None else _id #randomly,32char
        self.created_date = created_date


    # INSERT a SPECIFIC POST
    def save_to_mongo(self):
        Database.insert(collection='posts',
                        query=self.json())

    # get JSON/DATA of a SPECIFIC POST
    def json(self):
        return {
            '_id': self._id,
            'blog_id':self.blog_id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_date': self.created_date
        }
        #creates a json representation


    # Return a SPECIFIC POST
    @classmethod
    def from_mongo(cls, id):
        # Post.from_mongo('123')
        post_data = Database.find_one(collection='posts',query={'_id': id})
        return cls(**post_data)

    # Return the POSTS of a specific blog_id
    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]


