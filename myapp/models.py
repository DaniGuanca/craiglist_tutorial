from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    #para que muestre bonito el nombre
    def __str__(self):
        return self.search

    #Para que ponga bien en plural search, antes decia searchs ahora searches
    class Meta:
        verbose_name_plural = 'Searches'