import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, permission_required
from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    @permission_required('graphQl.view_link')
    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # 2
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # 3

    @login_required
    @permission_required('graphQl.add_link')
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


# 4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
