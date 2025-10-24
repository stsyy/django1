from django.db import models  

class Test(models.Model):
    name = models.CharField(max_length=255)  

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  
    question = models.CharField("Вопрос", max_length=500)
    answer = models.CharField("Правильный ответ", max_length=255)
    variants = models.TextField("Варианты")
    picture = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Изображение вопроса")
    
    def __str__(self):
        return f"Тест: {self.question[:30]}..."
  
class TestQuestionVariant(models.Model):
    test_question = models.ForeignKey("TestQuestion", on_delete=models.CASCADE) 
    text = models.CharField(max_length=255)  
    is_corect = models.BooleanField() 
    
class Result(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Ученик")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField("Баллы")  
    date = models.DateTimeField("Дата прохождения", auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.test}: {self.score} баллов"
        
class Student(models.Model):
    name = models.CharField("ФИО", max_length=255)  
    login = models.CharField("Логин", max_length=100)
    password = models.CharField("Пароль", max_length=100)
    level = models.CharField("Уровень", max_length=50)
    progress = models.IntegerField("Прогресс")
    picture = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="Фото студента")
        
    def __str__(self) -> str:
        return self.name