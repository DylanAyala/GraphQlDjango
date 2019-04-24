import graphene
import graphql_jwt
import Links.schema
import usr.schema


class Query(usr.schema.Query, Links.schema.Query, graphene.ObjectType):
    pass


class Mutation(usr.schema.Mutation, Links.schema.Mutation, graphene.ObjectType, ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
