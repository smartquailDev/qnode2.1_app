from django.db import models
from django.urls import reverse

class SubjectTest(models.Model):
    title = models.CharField(max_length = 200, db_index = True)
    slug = models.SlugField(max_length = 200, unique= True)

    class Meta:
        ordering =('title',)
        verbose_name = 'Subject test'
        verbose_name_plural = 'Subjects tests'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
            return reverse('courses_exams:test_list_by_subject_test',
                           args=[self.slug])

class Test(models.Model):
    subject_test = models.ForeignKey(SubjectTest, related_name ='tests',on_delete = models.CASCADE)
    question = models.CharField(max_length= 200, db_index= True)
    slug = models.SlugField(max_length= 200, db_index= True)
    image = models.ImageField(upload_to = 'test/%Y/%m/%d', blank= True)
    value = models.DecimalField(max_digits=10 , decimal_places=2)
    available = models.BooleanField(default=True)
    correct = models.BooleanField(default=True)

    class Meta:
        ordering = ('question',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
            return reverse('courses_exams:test_detail',
                           args=[self.id, self.slug])

class Instrucciones(models.Model):
    Title_A = models.CharField(max_length= 200)
    coment_A = models.CharField(max_length= 500)
    image_A = models.ImageField(upload_to = 'instrucciones_A/%Y/%m/%d', blank= True)
    Title_B = models.CharField(max_length= 200)
    coment_B = models.CharField(max_length= 500)
    image_B = models.ImageField(upload_to = 'instrucciones_B/%Y/%m/%d', blank= True)
    Title_C = models.CharField(max_length= 200)
    coment_C = models.CharField(max_length= 500)
    image_C = models.ImageField(upload_to = 'instrucciones_C/%Y/%m/%d', blank= True)
    Title_D = models.CharField(max_length= 200)
    coment_D = models.CharField(max_length= 500)
    image_D = models.ImageField(upload_to = 'instrucciones_D/%Y/%m/%d', blank= True)

    def __str__(self):
        return self.Title_A
