from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models import F, Q
from django.db.models.aggregates import Count, Max
from django.db.models.expressions import RawSQL
import random


class VerbManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Verb(models.Model):
    objects = VerbManager()

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class MoodManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Mood(models.Model):
    objects = MoodManager()

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class TenseManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Tense(models.Model):
    objects = TenseManager()

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class MoodTenseManager(models.Manager):
    def get_by_natural_key(self, mood, tense):
        return self.get(mood__name=mood, tense__name=tense)

class MoodTense(models.Model):
    objects = MoodTenseManager()

    mood = models.ForeignKey(Mood)
    tense = models.ForeignKey(Tense)

    def __str__(self):
        return "MoodTense({}, {})".format(str(self.mood), str(self.tense))

class PersonManager(models.Manager):
    def get_by_natural_key(self, number, index):
        return self.get(number=number, index=index)

class Person(models.Model):
    objects = PersonManager()

    SINGULAR = 's'
    PLURAL = 'p'
    NUMBER_CHOICES = (
        (SINGULAR, 'singulier'),
        (PLURAL, 'pluriel')
    )

    number = models.CharField(max_length=1, choices=NUMBER_CHOICES)
    index = models.PositiveSmallIntegerField() # 1, 2 or 3

    PRONOUNS = [['je'], ['tu'], ['il', 'elle', 'on'], ['nous'], ['vous'], ['ils', 'elles']]

    def __str__(self):
        return "Person({0.number}, {0.index})".format(self)

    def number_(self):
        return 'singulier' if self.number == Person.SINGULAR else 'pluriel'

    def pronoun(self):
        index = self.index - 1
        if self.number == Person.PLURAL:
            index += 3
        return Person.PRONOUNS[index]

    class Meta:
        unique_together = ('number', 'index')

class ConjugationManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return self.order_by('id')[random_index]

    def get_by_natural_key(self, verb, mood, tense, number, index):
        return self.get(
            verb__name=verb,
            mood_tense__mood__name=mood,
            mood_tense__tense__name=tense,
            person__number=number,
            person__index=index
        )

class Conjugation(models.Model):
    objects = ConjugationManager()

    verb = models.ForeignKey(Verb)
    mood_tense = models.ForeignKey(MoodTense)
    person = models.ForeignKey(Person)

    class Meta:
        unique_together = ('verb', 'mood_tense', 'person')

    def __str__(self):
        return "Conjugation(" + ", ".join([str(self.id), str(self.verb), str(self.mood_tense), str(self.person)]) + ")"

    def mood(self):
        return self.mood_tense.mood

    def tense(self):
        return self.mood_tense.tense

class ConjugationValue(models.Model):
    conjugation = models.ForeignKey(Conjugation, related_name='values')
    value = models.CharField(max_length=50)

    def __str__(self):
        return "ConjugationValue(" + str(self.value) + ")"

    class Meta:
        unique_together = ('conjugation', 'value')


class AttemptQuerySet(models.query.QuerySet):

    def own(self, request):
        if not request.user.is_anonymous():
            return self.filter(user=request.user)

        if request.session.session_key is None:
            return self.none()

        return self.filter(user_session_id=request.session.session_key)

    def num_attempts(self, request):
        return self.own(request).count()

    def num_good_attempts(self, request):
        return self.own(request).filter(answer=F('conjugation__values__value')).count()


class Attempt(models.Model):
    objects = AttemptQuerySet.as_manager()
    conjugation = models.ForeignKey(Conjugation)
    answer = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, on_delete=models.SET_NULL, null=True, blank=True)
    user_session = models.ForeignKey(Session, db_index=True, on_delete=models.SET_NULL, null=True, blank=True)

    def is_good(self):
        return self.conjugation.values.filter(value=self.answer).exists()

    def values(self):
        return [v['value'] for v in self.conjugation.values.all().values('value')]

    def __str__(self):
        return "Attempt(" + ", ".join([str(self.conjugation), "[" + ", ".join(str(v) for v in self.conjugation.values.all()) + "]", str(self.answer)]) + ")"
