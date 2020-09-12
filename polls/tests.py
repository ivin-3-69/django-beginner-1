import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question,Choice

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_question = Question(pub_date = timezone.now() + datetime.timedelta(days=30))
        self.assertIs(future_question.latest_publishment(), False)
    
    def test_was_published_recently_with_recent_question(self):
        present_question = Question(pub_date = timezone.now())
        present_question1 =Question(pub_date = timezone.now() - datetime.timedelta(hours=23,minutes=59 ,seconds=59))
        self.assertIs(present_question.latest_publishment(),True)
    
    def test_was_published_recently_with_older_question(self):
        older_question   = Question(pub_date = timezone.now() - datetime.timedelta(days=1,seconds=2))
        self.assertIs(older_question.latest_publishment(),False)