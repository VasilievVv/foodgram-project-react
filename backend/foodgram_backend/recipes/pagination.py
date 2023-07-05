from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Кастомный пагинатор, с переопределенным параметром 'page_size'."""
    page_size = 3
    page_size_query_param = 'limit'
