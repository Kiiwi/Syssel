from haystack import indexes
from .models import Job


class JobIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Indexing all jobs
    """
    text = indexes.EdgeNgramField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='headline')

    def get_model(self):
        """
        Method to get model
        :return: Model
        """
        return Job

    def index_queryset(self, using=None):
        """
        Method to set queryset
        :param using:
        :return: Queryset
        """
        return self.get_model().objects.all()