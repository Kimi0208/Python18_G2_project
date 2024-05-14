import factory
from factory.django import DjangoModelFactory
from webapp.models import Comment
from webapp.tests.factories.user import DefUserFactory
from webapp.tests.factories.task import TaskFactory


class CommentFactory(DjangoModelFactory):
    description = factory.Sequence(lambda n: f'Description {n}')
    task = factory.SubFactory(TaskFactory)
    author = factory.SubFactory(DefUserFactory)

    class Meta:
        model = Comment
