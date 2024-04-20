import factory
from factory.django import DjangoModelFactory
from webapp.models import Task, Type, Status, Priority


class TypeFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Type {n}")

    class Meta:
        model = Type


class StatusFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Status {n}")

    class Meta:
        model = Status


class TaskFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f'Task {n}')
    type = factory.SubFactory(TypeFactory)
    description = factory.Sequence(lambda n: f'Description {n}')
    status = factory.SubFactory(StatusFactory)

    class Meta:
        model = Task


class PriorityFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Priority {n}")

    class Meta:
        model = Priority