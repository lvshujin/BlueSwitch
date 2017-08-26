from django.db.models import Q


class DatatableSearchMixin(object):
    """
    Search datatable based on provided serach columns if provided otherwise based on datatable's columns.
    """
    search_columns = []

    def filter_queryset(self, qs):
        """
        The filtering of the queryset with respect to the search keyword entered.

        :param qs:
        :return qs:

        """
        sSearch = self.request.GET.get('search[value]', None)
        if sSearch:
            search_columns = self.search_columns if self.search_columns else self.columns

            query_object = Q()
            for column in search_columns:
                query_object = query_object | Q(**{"%s__icontains" % column: sSearch})
            qs = qs.filter(query_object).distinct()
        return qs
