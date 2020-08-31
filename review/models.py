from datetime import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from datetime import date, datetime
from notifications.models import Notification
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    vote = models.FloatField()
    desc = models.TextField()
    image = models.ImageField(upload_to='book_pics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def get_vote(self):
        if self.vote == int(self.vote):
            self.vote = int(self.vote)
        else:
            self.vote = int(round(self.vote))
        return self.vote

    @property
    def actual_rating(self):
        list_of_stars = []
        for star in range(self.get_vote()):
            list_of_stars.append(star)
        return list_of_stars

    @property
    def hidden_rating(self):
        list_of_stars = []
        for star in range(5 - self.get_vote()):
            list_of_stars.append(star)
        return list_of_stars

class BookMark(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'user',)

    MARK_STATUS = (
        ('nr', 'Not read'),
        ('r_ed', 'Readed'),
        ('r_ing', 'Reading'),
    )
    mark_status = models.CharField(
        max_length=5,
        choices=MARK_STATUS,
        blank=True,
        default='nr',
        help_text='Book has not been read',
    )

    FAVORITE_STATUS = (
        ('fa', 'Favorite'),
        ('un_fa', 'Unfavorite'),
    )
    fa_status = models.CharField(
        max_length=5,
        choices=FAVORITE_STATUS,
        blank=True,
        default='un_fa',
        help_text='Book has not been mark favorite'
    )

    # activ : get_str ---->>>> 


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    REQUEST_STATUS = (
        ('rv', 'Reviewing'),
        ('a', 'Approved'),
        ('rj', 'Reject'),
    )

    status = models.CharField(
        max_length=2,
        choices=REQUEST_STATUS,
        blank=True,
        default='rv',
        help_text='Request is reviewing',
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    def save(self):
        if self.pk is not None:
            request_after = Request.objects.get(id = self.id)
            sender_user = User.objects.filter(is_staff=True)[0]
            print(sender_user)
            to_user = self.user
            print(to_user)
            if request_after.status == 'rj':
                notify = Notification(sender = sender_user,user=to_user, notification_type=1, text_preview='Reject  your request book with title {}'.format(self.title))
                notify.save()
            elif request_after.status == 'a':
                notify = Notification(sender = sender_user, user = to_user, notification_type=1, text_preview='Approved your request book with title {}'.format(self.title))
                notify.save()
        return super(Request, self).save()







class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    RATE_CHOICE = (
        (1, 'Awful'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Great'),
        (5, 'Excellent'),
    )
    star = models.IntegerField(
        choices=RATE_CHOICE,
        default=5,
    )
    # review_id = models.AutoField(primary_key=True)
    review = models.TextField()
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' reviewed ' + self.book.title

    @property
    def actual_rating(self):
        list_of_stars = []
        for star in range(self.star):
            list_of_stars.append(star)
        return list_of_stars

    @property
    def hidden_rating(self):
        list_of_stars = []
        for star in range(5 - self.star):
            list_of_stars.append(star)
        return list_of_stars

    def get_id(self):
        return self.get_id()

class Comment(models.Model):
    rate = models.ForeignKey(Rating, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

from django.contrib.auth import get_user_model
UserModel = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return '%s follows %s' % (self.follower, self.following)


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ACTIVITY_TYPE = (
        ('fo', 'Follow'),
        ('fa', 'Favorite'),
        ('un_fo', 'Unfollow'),
        ('un_fa', 'Unfavorite'),
        ('ma_ed', 'Mark read'),
        ('ma_ing', 'Mark reading'),
        ('rv', 'Review')
    )
    activity_type = models.CharField(
        max_length=200,
        choices=ACTIVITY_TYPE,
        blank=True,
    )
    activity = models.TextField()
