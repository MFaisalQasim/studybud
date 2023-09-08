from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request):
	routes = [
		'GET /api',
		'GET /api/rooms',
		'GET /api/room/:id' 
	]
	return Response(routes)


@api_view(['GET'])
def getRooms(request):
	rooms = Room.objects.all()
	serilizer = RoomSerializer(rooms, many=True)
	return Response(serilizer.data)

@api_view(['GET', 'POST'])
def getRooms(request, id):
	room = Room.objects.get(id=id)
	serilizer = RoomSerializer(room)
	return Response(serilizer.data)