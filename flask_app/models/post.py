from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    db_name = 'volunteer'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.contact = data['contact']
        self.location = data['location']
        self.link = data['linki']
        self.user_id = data['user_id']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_post_by_id(cls, data):
        query = "SELECT * FROM posts WHERE posts.id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
      #READ
    @classmethod
    def get_all(cls):
        query = "SELECT posts.*, users.first_name, users.last_name, COUNT(saves.post_id) as num_saves FROM posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN saves ON posts.id = saves.post_id GROUP BY posts.id ORDER BY created_at DESC;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        posts = []
        if results:
        # Iterate over the db results and create instances of friends with cls.
            for post in results:
                posts.append(post)
            return posts
        return posts
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (name, description, location, linki, contact, image, user_id) VALUES ( %(name)s, %(description)s, %(location)s ,%(linki)s, %(contact)s, %(image)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET name = %(name)s, description = %(description)s,location = %(location)s, linki = %(linki)s, contact = %(contact)s, image = %(image)s WHERE posts.id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
     
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE posts.id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
        #DELETE
    @classmethod
    def deleteAllSaves(cls, data):
        query = "DELETE FROM saves WHERE post_id = %(post_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

     #add save
    @classmethod
    def addSave(cls, data):
        query = "INSERT INTO saves (post_id, user_id) VALUES ( %(post_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def unSave(cls, data):
        query = "DELETE FROM saves WHERE post_id = %(post_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    

    @classmethod
    def get_post_savers(cls, data):
        query = "SELECT * from saves LEFT JOIN users on saves.user_id = users.id WHERE post_id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfSaves = []
        if results:
            for row in results:
                nrOfSaves.append(row['email'])
            return nrOfSaves
        return nrOfSaves
    

    @staticmethod
    def validate_post(post):
        is_valid = True
        
        if len(post['name']) <2:
            flash('Title should be more than 2 characters!', 'namePost')
            is_valid= False
        if len(post['description']) <2:
            flash('Description should be more than 2 characters!', 'descriptionPost')
            is_valid= False
        if len(post['contact']) <=0:
            flash('Please include a way to contact you!', 'contactPost')
            is_valid= False
        if not post.get('location'):
            flash('Please include location', 'locationPost')
            is_valid = False
        if not post.get('linki'):
            flash('Please include location', 'linkiPost')
            is_valid = False

        return is_valid