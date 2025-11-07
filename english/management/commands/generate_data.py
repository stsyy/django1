# english/management/commands/generate_data.py

from django.core.management.base import BaseCommand
from faker import Faker
from english.models import Student, Test, TestQuestion, TestQuestionVariant, Result
import random
from django.db import transaction 

class Command(BaseCommand):
    help = 'Generates 1000 records for all main models'

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        levels = ["Начальный", "Средний", "Продвинутый"]

        with transaction.atomic():
            
            self.stdout.write(self.style.NOTICE('Очистка старых данных...'))
            Student.objects.all().delete()
            Test.objects.all().delete()

            self.stdout.write(self.style.NOTICE('Генерация 1000 студентов...'))
            students_to_create = []
            for i in range(1000):
                students_to_create.append(Student(
                    name=fake.name(),
                    login=f'student_{i}_{fake.word()}',
                    password='testpassword123',
                    level=random.choice(levels),
                    progress=random.randint(0, 100)
                ))
            Student.objects.bulk_create(students_to_create)
            
            self.stdout.write(self.style.NOTICE('Генерация 50 тестов...'))
            tests_to_create = []
            for i in range(50):
                tests_to_create.append(Test(name=f"Тест по Английскому #{i+1} ({random.choice(levels)})"))
            Test.objects.bulk_create(tests_to_create)
            
            all_tests = list(Test.objects.all())

            self.stdout.write(self.style.NOTICE('Генерация 1000 вопросов...'))
            questions_to_create = []
            
            for i in range(1000):
                test = random.choice(all_tests)
                correct_answer = fake.sentence(nb_words=3)
                questions_to_create.append(TestQuestion(
                    test=test,
                    question=fake.sentence(nb_words=10),
                    answer=correct_answer,
                    variants=f'Вариант 1, Вариант 2, {correct_answer}, Вариант 4' 
                ))
            TestQuestion.objects.bulk_create(questions_to_create)
            
            all_questions = list(TestQuestion.objects.all())
            
            self.stdout.write(self.style.NOTICE('Генерация 4000 вариантов вопросов...'))
            variants_to_create = []
            
            for question in all_questions:
    
                for _ in range(3):
                    variants_to_create.append(TestQuestionVariant(
                        test_question=question,
                        text=fake.sentence(nb_words=3),
                        is_corect=False
                    ))

                variants_to_create.append(TestQuestionVariant(
                    test_question=question,
                    text=question.answer, 
                    is_corect=True
                ))
            TestQuestionVariant.objects.bulk_create(variants_to_create)

            self.stdout.write(self.style.NOTICE('Генерация 1000 результатов...'))
            all_students = list(Student.objects.all()) # Обновляем список студентов
            results_to_create = []
            
            for i in range(1000):
                results_to_create.append(Result(
                    student=random.choice(all_students),
                    test=random.choice(all_tests),
                    score=random.randint(5, 50), # Баллы от 5 до 50
                ))
            Result.objects.bulk_create(results_to_create)

            self.stdout.write(self.style.SUCCESS('\nВсе данные успешно сгенерированы!'))