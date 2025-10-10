from django.db import models

class Word(models.Model):
    word = models.CharField("Слово")
    translation = models.CharField("Перевод")
    picture = models.ImageField("Картинка")
    topic = models.CharField("Тема")
    
    def __str__(self):
        return f"{self.word} - {self.translation}"
    
class Test(models.Model):
    question = models.CharField("Вопрос")
    answer = models.CharField("Правильный ответ")
    variants = models.TextField("Варианты")
    
    def __str__(self):
        return f"Тест: {self.question[:30]}..."  
  
    
class Result(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name="Ученик")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField("Баллы")  
    date = models.DateTimeField("Дата прохождения", auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.test}: {self.score} баллов"
        
class Lesson(models.Model):
    ltopic = models.CharField("Тема урока")
    ltest = models.DateField("Дата")  
    homework = models.TextField("Домашнее задание")
    words = models.ManyToManyField(Word, verbose_name="Список слов")
    test = models.OneToOneField(Test, on_delete=models.SET_NULL, null=True, blank=True, 
                              verbose_name="Тест урока", related_name='lesson')
    def __str__(self):
        return f"Урок: {self.ltopic} ({self.ltest})"
    
class Student(models.Model):
    name = models.CharField("ФИО")
    login = models.CharField("Логин")
    password = models.CharField("Пароль")
    level = models.CharField("Уровень")
    progress = models.IntegerField("Прогресс")
        
    def __str__(self) -> str:
        return self.name