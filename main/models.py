from django.db import models
from django.db import IntegrityError

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        emails = Users.objects.all().values('email')
        if len(postData['first_name'])< 2:
            errors["first_name"] = f'{["first_name"]} is not a name, try it again with 4 characters at least'
        if postData['email'] in emails:
            errors["email"] = f'This email already exist'
        if len(postData['last_name'])< 2:
            errors["last_name"] = "'Last Name' should be at least 4 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors["password"] = "Both passwords have to be equals"
        
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=255)
    avatar = models.URLField()
    allowed = models.BooleanField(default=True)
    #followers
    followed = models.ManyToManyField('Users', related_name='followers')
    # messsages
    # comments
    objects = UsersManager()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self) -> str:
        return f'{self.id}: {self.first_name} {self.last_name}'
    
class Publishers(models.Model):
    publish = models.TextField()
    author = models.ForeignKey(Users, related_name="publishers", on_delete=models.CASCADE)
    # comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self) -> str:
        return f'[{self.id}] {self.author.first_name}'

class Comments(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(Users, related_name="comments", on_delete=models.CASCADE)
    publish = models.ForeignKey(Publishers, related_name="comments", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self) -> str:
        return f'[{self.id}] {self.author}'

