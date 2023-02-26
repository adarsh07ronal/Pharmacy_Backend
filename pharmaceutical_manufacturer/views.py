# Create your views here.
from rest_framework import viewsets
from .models import PharmaceuticalManufacturer,PublicationPlace , PostingType
from .serializers import *
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class PharmaceuticalManufacturerViewset(viewsets.ModelViewSet):
    """
    CRUD operations for Pharmaceutical Manufacturer

    Authentication Required : YES

    Request Data : {
        "listed_company_name" :"",
        "manager":"",
        "email":"",
        "telephone_number":"",
        "post_period_start":"",
        "post_period_end":"",
        "place_of_publication":1
        "posting_type":1,
        "advertising_text":"",
        "banner": Upload a file,
        "link_destination":""
    }
    """
 
    queryset = PharmaceuticalManufacturer.objects.all()
    serializer_class = PharmaceuticalManufacturerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['id']
    parser_classes = [MultiPartParser,JSONParser]
    # pagination_class = None

    def create(self, request):
        data = self.request.data            
        serializer = PharmaceuticalManufacturerCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            manf_obj = PharmaceuticalManufacturer.objects.filter(id=pk)
            if manf_obj.count():
                manf_obj = manf_obj.first()
                data = request.data
                serializer = PharmaceuticalManufacturerBannerNullSerializer(manf_obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data = serializer.data ,status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"No Advertisement data found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AdvertisementListingViewset(viewsets.ModelViewSet):
    queryset = PharmaceuticalManufacturer.objects.all()
    serializer_class = PharmaceuticalManufacturerSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        qs = self.queryset
        for q in qs:
            q.no_of_exposures+=1
            q.save()
        return Response(data=self.serializer_class(qs,many=True).data,status=status.HTTP_200_OK)

class ClicksCounterAPIView(APIView):
    """
    Clicks Counter API View

    Authentication Required : YES

    Request Data : {
        "id" : 1
    }
    """    
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        data = self.request.data
        ad_objs = PharmaceuticalManufacturer.objects.filter(id=data["id"])
        if ad_objs.count():
            ad_obj = ad_objs.first()
            ad_obj.no_of_clicks+=1 
            ad_obj.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class PPListAPI(APIView):
    """
    List of PlacePublications and Posting Types

    Authentication Required : NO
    """    

    def get(self,request,*args,**kwargs):
        PlacePublications_ins = PublicationPlace.objects.all()
        pub_serializer = PublicationPlaceSerializer(PlacePublications_ins,many=True)
        postingtype_ins = PostingType.objects.all()
        pos_serializer = PostingTypeSerializer(postingtype_ins,many=True)
        pp_l = {"place_of_publication":pub_serializer.data,"posting_type" :pos_serializer.data}
        return Response(pp_l, status=status.HTTP_200_OK)