from django.db import models  

class Test(models.Model):
    name = models.CharField(max_length=255)  
    user=models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField("Вопрос", max_length=500)
    picture = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Изображение вопроса")
    user=models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Тест: {self.question[:30]}..."
    
class Tutor(models.Model):
    user = models.OneToOneField("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE) 
    name = models.CharField("ФИО", max_length=255)  
    def __str__(self):
        return self.name    
  
class TestQuestionVariant(models.Model):
    test_question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name='variants')
    text = models.CharField(max_length=255)  
    is_correct = models.BooleanField() 
    user=models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    
class Result(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Ученик")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField("Баллы")  
    date = models.DateTimeField("Дата прохождения", auto_now_add=True)
    user=models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.student} - {self.test}: {self.score} баллов"
        
class Student(models.Model):
    name = models.CharField("ФИО", max_length=255)  
    login = models.CharField("Логин", max_length=100)
    password = models.CharField("Пароль", max_length=100)
    level = models.CharField("Уровень", max_length=50)
    progress = models.IntegerField("Прогресс")
    picture = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="Фото студента")
    user=models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    tutor = models.ForeignKey("auth.User",on_delete=models.SET_NULL,null=True,blank=True,related_name='students',limit_choices_to={'userprofile__type': 'tutor'})
    assigned_tests = models.ManyToManyField(Test, blank=True, verbose_name="Назначенные тесты")    
    def __str__(self):
        return f"Студент id: {self.id} ФИО: {self.name}"
    
   