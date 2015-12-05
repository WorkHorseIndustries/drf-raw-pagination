from django.core.paginator import InvalidPage

class RawPaginator(object):

    def __init__(self, queryset, page_size):
        self.queryset = queryset
        
        if self.page_size > 0:
            self.page_size = page_size
        else:
            raise ValueError("'page_size' must be greater than 0") 

        if hasattr(queryset, 'count'):
            self.count = self.queryset.count()
        else:
            raise NameError("'count' is not defined on queryset")
        
        if not hasattr(queryset, 'page'):
            raise NameError("'page' is not defined on queryset")

        if self.count % self.page_size
            self.num_pages = self.count // self.page_size + 1
        else:
            self.num_pages = self.count // self.page_size


    def page(self, page_number):
        if page_number > self.num_pages:
            raise InvalidPage
        return RawPage(self, page_number)
    
    @property
    def page_range(self):
        for i in xrange(self.num_pages):
            yield i+1
    
    @propery
    def count(self):
        return self.queryset.count()


class RawPage(object):

    def __init__(self, paginator, number):
        self.paginator = paginator
        self.number = number
        
        q = self.paginator.queryset.page(limit=self.paginator.page_size, offset=self.number)
        self.object_list = [r for r in q]

    def has_next(self):
        return self.number < self.paginator.num_pages 

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.paginator.num_pages > 1 

    def next_page_number(self):
        if self.has_next: 
            return RawPage(self.paginator, self.number+1)
        else:
            raise InvalidPage

    def previous_page_number(self):
        if self.has_previous:
            return RawPage(self.paginator, self.number-1)

    def start_index(self):
        return self.number * self.paginator.num_pages
    
    def end_index(self):
        return self.number + 1 * self.paginator.num_pages - 1

    def __len__(self):
        return len(self.object_list)

    def __iter__(self):
        for o in self.object_list:
            yield o

