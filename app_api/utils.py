from mongoengine import QuerySet


class PaginateQuerySet:
    """
    class for the implementation of pagination on the web page
    """
    def __init__(self, queryset:QuerySet, per_page:int, num_page:int=0):
        self.queryset = queryset
        self.per_page = per_page
        self.num_page = num_page
        self.ofset = (self.num_page - 1) * self.per_page
        self.total_pages = round(len(self.queryset) / self.per_page)
    
    def get_queryset(self):
        return self.queryset.skip(self.ofset).limit(self.per_page)

    def has_next(self):
        return (self.num_page + 1) <= self.total_pages

    def has_prev(self):
        return (self.num_page - 1) >= 1

    def prev_num(self):
        if self.has_prev():
            return self.num_page - 1

    def next_num(self):
        if self.has_next():
            return self.num_page + 1
