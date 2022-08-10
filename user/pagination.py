from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 25
    page_query_param="page"
    page_size_query_param = 'page_size' 
    max_page_size = 200
    last_page_strings = ('the_end')