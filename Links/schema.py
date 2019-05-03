import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, permission_required
from .models import Link, Contact
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
import django_filters


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        filter_fields = {
            'id': ['exact'],
            'url': ['exact', 'icontains', 'istartswith'],
            'description': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    link = DjangoFilterConnectionField(LinkNode)
    contact = graphene.List(ContactType)

    @permission_required('graphQl.view_link')
    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    @permission_required('graphQl.view_link')
    def resolve_link(self, info, url):
        return Link.objects.filter(url=url)

    def resolve_contact(self, info):
        return Contact.objects.all()


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


class CreateContact(graphene.Mutation):
    contact = graphene.Field(ContactType)

    class Arguments:
        name = graphene.String()
        phone = graphene.Int()
        email = graphene.String()

    def mutate(self, info, name, phone, email):
        contact = Contact(name=name, phone=phone, email=email)
        contact.save()
        return CreateContact(contact=contact)


class UpdateContact(graphene.Mutation):
    contact = graphene.Field(ContactType)

    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        phone = graphene.Int()
        email = graphene.String()

    def mutate(self, info, id, name, phone, email):
        contact = Contact.objects.filter(id=id)
        if contact:
            contact.update(name=name, phone=phone, email=email)
        else:
            raise Exception('no se encontro el usuario con el id suministrado')
        if contact:
            contact = Contact(id=id, name=name, phone=phone, email=email)
        else:
            raise Exception('No se se puedo editar')
        return UpdateContact(contact=contact)


# 4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_contact = CreateContact.Field()
    update_contact = UpdateContact.Field()
