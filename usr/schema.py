from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import Group, Permission
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)
    group = graphene.Field(graphene.List(GroupType))
    permission = graphene.List(PermissionType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_group(self, info):
        return Group.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

    def resolve_permission(self, info):
        return Permission.objects.all()


class CreateGroup(graphene.Mutation):
    group = graphene.Field(GroupType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    @login_required
    def mutate(self, info, name):
        group = Group.objects.get_or_create(
            name=name)
        return CreateGroup(group=group)


class UserGroup(graphene.Mutation):
    group = graphene.Field(GroupType)
    user = graphene.Field(UserType)

    class Arguments:
        user = graphene.String()
        name = graphene.String()

    @login_required
    def mutate(self, info, user, name):
        group = Group.objects.get(name=name)
        group.user_set.add(user)
        return UserGroup(group=group)


class PermissionGroup(graphene.Mutation):
    group = graphene.Field(GroupType)
    permission = graphene.Field(PermissionType)

    class Arguments:
        permission = graphene.String()
        name = graphene.String()

    @login_required
    def mutate(self, info, permission, name):
        group = Group.objects.get(name=name)
        group.permissions.add(permission)
        return UserGroup(group=group)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_group = CreateGroup.Field()
    user_group = UserGroup.Field()
    permission_group = PermissionGroup.Field()
