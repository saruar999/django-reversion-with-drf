from reversion.models import Version
from reversion.views import RevisionMixin
from reversion.errors import RegistrationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from blog.revision.serializers import RevisionSerializer, RevisionRevertSerializer


class CustomRevisionMixin(RevisionMixin):

    def get_versions(self):
        instance = self.get_object()
        try:
            versions = Version.objects.get_for_object(instance)
        except RegistrationError:
            raise APIException(detail='model has not been registered for revision.')
        current_version = versions[0]
        versions = versions.exclude(pk=current_version.id)
        return instance, versions

    @action(methods=['GET'], detail=True)
    def instance_logs(self, request, **kwargs):
        instance, versions = self.get_versions()
        serializer = RevisionSerializer(versions, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def revert_instance(self, request, **kwargs):
        instance, versions = self.get_versions()
        serializer = RevisionRevertSerializer(instance, data=request.data, context={'versions': versions})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        version = serializer.validated_data.get('version')
        return Response({'message': 'instance reverted to version %d.' % version.id})
