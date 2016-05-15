from haystack import indexes
from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Indexing all users
    """
    text = indexes.EdgeNgramField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='username')

    def get_model(self):
        """
        Method to get model
        :return: Model
        """
        return User

    def index_queryset(self, using=None):
        """
        Method to set queryset
        :param using:
        :return: Queryset
        """
        return self.get_model().objects.all()