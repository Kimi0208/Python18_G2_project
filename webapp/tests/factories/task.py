import factory
from factory.django import DjangoModelFactory
from webapp.models import Task, Type, Status, Priority
from webapp.tests.factories.user import DefUserFactory


class TypeFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Type {n}")

    class Meta:
        model = Type


class StatusFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Status {n}")

    class Meta:
        model = Status


class PriorityFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Priority {n}")

    class Meta:
        model = Priority


class TaskFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f'Task {n}')
    type = factory.SubFactory(TypeFactory)
    description = factory.Sequence(lambda n: f'Description {n}')
    priority = factory.SubFactory(PriorityFactory)
    status = factory.SubFactory(StatusFactory)
    author = factory.SubFactory(DefUserFactory)

    class Meta:
        model = Task


