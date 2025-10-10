from django.db import models  
    
class Test(models.Model):
    name = models.CharField()    

class TestQuestion(models.Model):
    test = models.ForeignKey(Test)
    question = models.CharField("Вопрос")
    answer = models.CharField("Правильный ответ")
    variants = models.TextField("Варианты")
    
    def __str__(self):
        return f"Тест: {self.question[:30]}..."  
  
  
class TestQuestionVariant(models.Model):
    test_question = models.ForeignKey("TestQuestion")
    text = models.CharField()
    is_corect = models.BooleanField() 
    
class Result(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Ученик")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField("Баллы")  
    date = models.DateTimeField("Дата прохождения", auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.test}: {self.score} баллов"
        
#привязать к юзеру  
class Student(models.Model):
    name = models.CharField("ФИО")
    login = models.CharField("Логин")
    password = models.CharField("Пароль")
    level = models.CharField("Уровень")
    progress = models.IntegerField("Прогресс")
        
    def __str__(self) -> str:
        return self.name