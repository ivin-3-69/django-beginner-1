import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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

    
def create_question(question_text, daysoffset):
    time = timezone.now() + datetime.timedelta(days=daysoffset)
    return Question.objects.create(question_text= question_text,pub_date = time)

class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_past_question(self):
        create_question(question_text="Past question.",daysoffset=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        create_question("Future question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_future_and_past_question(self):
        create_question(question_text="Past question.", daysoffset=-30)
        create_question("Future question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_question(self):
        create_question(question_text="Past question 1.",daysoffset=-30)
        create_question(question_text="Past question 2.",daysoffset=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class DetailViewTest(TestCase):
    def test_future_question(self):
        future_question = create_question("Future question.", 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past question 1.",daysoffset=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
