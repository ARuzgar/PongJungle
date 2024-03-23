from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MatchSerializer
from .models import Match


def JsonProviderBasic(success, message, **kwargs):
    d = {
        "success": success,
        "data": None,
        "message": message,
        "error": None,
    }
    if "data" in kwargs and kwargs["data"] is not None:
        d.update({"data": kwargs["data"]})
    if "error" in kwargs and kwargs["error"] is not None:
        d.update({"error": kwargs["error"]})
    return d


class MatchCreateAndList(APIView):

    def get(self, request):
        print('matches: ', request.GET.get('username'))
        matches = Match.objects.filter(username=request.GET.get('username'))
        serializer = MatchSerializer(matches, many=True)
        if not matches:
            return Response(
                JsonProviderBasic(
                    False,
                    "No matches found.",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            JsonProviderBasic(
                True,
                "Matches retrieved successfully.",
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = MatchSerializer(data=request.data)
        print('request.data: ', request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                JsonProviderBasic(
                    True,
                    "Match created successfully.",
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            JsonProviderBasic(
                False,
                "Match could not be created.",
                error=serializer.errors,
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )
