from django.db import models
from django.core.validators import MaxLengthValidator

class Resume(models.Model):
  
  file_name = models.CharField("Nome do arquivo", max_length=150, blank=False, null=False)
  resume = models.TextField("Resumo feito", validators=[MaxLengthValidator(3000)], blank=True, null=True)
  is_resumed = models.BooleanField("Esse pdf ja foi resumido?", default=False)
  created_at = models.DateTimeField("Data de criação", auto_now_add=True ,blank=False, null=False)
  updated_at = models.DateTimeField("Data de atualização", auto_now=True ,blank=False, null=False)
  
  def __str__(self):
    return self.file_name