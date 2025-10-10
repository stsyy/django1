from django.test import TestCase
from rest_framework.test import APIClient
from english.models import Student, Word, Test, Result, Lesson
from model_bakery import baker


class StudentViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        student = baker.make("Student")
        r = self.client.get('/api/students/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(student.name, data[0]['name'])
        self.assertEqual(student.id, data[0]['id'])
        self.assertEqual(student.login, data[0]['login'])
        self.assertEqual(student.level, data[0]['level'])
        self.assertEqual(student.progress, data[0]['progress'])

    def test_get_single(self):
        student = baker.make("Student")
        r = self.client.get(f'/api/students/{student.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['id'], student.id)
        self.assertEqual(data['name'], student.name)
        self.assertEqual(data['login'], student.login)

    def test_create_student(self):
        student_data = {
            "name": "Тестовый Студент",
            "login": "test_user",
            "password": "test_password",
            "level": "A1",
            "progress": 0
        }
        r = self.client.post('/api/students/', student_data, format='json')
        self.assertEqual(r.status_code, 201)
        
        data = r.json()
        self.assertEqual(data['name'], student_data['name'])
        self.assertEqual(data['login'], student_data['login'])
        self.assertEqual(data['level'], student_data['level'])
        self.assertEqual(data['progress'], student_data['progress'])

    def test_update_student(self):
        student = baker.make("Student")
        update_data = {"name": "Семён Лыхин"}
        r = self.client.patch(f'/api/students/{student.id}/', update_data, format='json')
        self.assertEqual(r.status_code, 200)

        r = self.client.get(f'/api/students/{student.id}/')
        data = r.json()
        self.assertEqual(data['name'], "Семён Лыхин")

        student.refresh_from_db()
        self.assertEqual(student.name, "Семён Лыхин")

    def test_delete_student(self):
        student = baker.make("Student")
        r = self.client.delete(f'/api/students/{student.id}/')
        self.assertEqual(r.status_code, 204)

        r = self.client.get('/api/students/')
        data = r.json()
        self.assertEqual(len(data), 0)


class WordViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        word = baker.make("Word")
        r = self.client.get('/api/words/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(word.word, data[0]['word'])
        self.assertEqual(word.translation, data[0]['translation'])

    def test_get_single(self):
        word = baker.make("Word")
        r = self.client.get(f'/api/words/{word.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['id'], word.id)
        self.assertEqual(data['word'], word.word)
        self.assertEqual(data['translation'], word.translation)

    def test_create_word(self):
        word_data = {
            "word": "apple",
            "translation": "яблоко",
            "topic": "Фрукты",
            "level": "A1"
        }
        r = self.client.post('/api/words/', word_data, format='json')
        self.assertEqual(r.status_code, 201)
        
        data = r.json()
        self.assertEqual(data['word'], word_data['word'])
        self.assertEqual(data['translation'], word_data['translation'])
        self.assertEqual(data['topic'], word_data['topic'])

    def test_update_word(self):
        word = baker.make("Word")
        update_data = {"topic": "Фрукты"}
        r = self.client.patch(f'/api/words/{word.id}/', update_data, format='json')
        self.assertEqual(r.status_code, 200)
        
        word.refresh_from_db()
        self.assertEqual(word.topic, "Фрукты")

    def test_delete_word(self):
        word = baker.make("Word")
        r = self.client.delete(f'/api/words/{word.id}/')
        self.assertEqual(r.status_code, 204)

        r = self.client.get('/api/words/')
        data = r.json()
        self.assertEqual(len(data), 0)


class TestViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        test = baker.make("Test")
        r = self.client.get('/api/tests/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(test.question, data[0]['question'])
        self.assertEqual(test.answer, data[0]['answer'])

    def test_get_single(self):
        test = baker.make("Test")
        r = self.client.get(f'/api/tests/{test.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['id'], test.id)
        self.assertEqual(data['question'], test.question)
        self.assertEqual(data['answer'], test.answer)

    def test_create_test(self):
        test_data = {
            "question": "What is the capital of Great Britain?",
            "answer": "London",
            "option1": "Paris",
            "option2": "Berlin",
            "option3": "Madrid",
            "lesson": None
        }
        r = self.client.post('/api/tests/', test_data, format='json')
        self.assertEqual(r.status_code, 201)
        
        data = r.json()
        self.assertEqual(data['question'], test_data['question'])
        self.assertEqual(data['answer'], test_data['answer'])
        self.assertEqual(data['option1'], test_data['option1'])

    def test_update_test(self):
        test = baker.make("Test")
        update_data = {"answer": "London"}
        r = self.client.patch(f'/api/tests/{test.id}/', update_data, format='json')
        self.assertEqual(r.status_code, 200)
        
        test.refresh_from_db()
        self.assertEqual(test.answer, "London")

    def test_delete_test(self):
        test = baker.make("Test")
        r = self.client.delete(f'/api/tests/{test.id}/')
        self.assertEqual(r.status_code, 204)

        r = self.client.get('/api/tests/')
        data = r.json()
        self.assertEqual(len(data), 0)


class LessonViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        lesson = baker.make("Lesson")
        r = self.client.get('/api/lessons/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(lesson.ltopic, data[0]['ltopic'])
        self.assertEqual(lesson.grammar, data[0]['grammar'])

    def test_get_single(self):
        lesson = baker.make("Lesson")
        r = self.client.get(f'/api/lessons/{lesson.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['id'], lesson.id)
        self.assertEqual(data['ltopic'], lesson.ltopic)
        self.assertEqual(data['grammar'], lesson.grammar)

    def test_create_lesson(self):
        lesson_data = {
            "ltopic": "Present Simple",
            "grammar": "Basic present tense",
            "level": "A1"
        }
        r = self.client.post('/api/lessons/', lesson_data, format='json')
        self.assertEqual(r.status_code, 201)
        
        data = r.json()
        self.assertEqual(data['ltopic'], lesson_data['ltopic'])
        self.assertEqual(data['grammar'], lesson_data['grammar'])
        self.assertEqual(data['level'], lesson_data['level'])

    def test_update_lesson(self):
        lesson = baker.make("Lesson")
        update_data = {"ltopic": "Past Simple"}
        r = self.client.patch(f'/api/lessons/{lesson.id}/', update_data, format='json')
        self.assertEqual(r.status_code, 200)
        
        lesson.refresh_from_db()
        self.assertEqual(lesson.ltopic, "Past Simple")

    def test_delete_lesson(self):
        lesson = baker.make("Lesson")
        r = self.client.delete(f'/api/lessons/{lesson.id}/')
        self.assertEqual(r.status_code, 204)

        r = self.client.get('/api/lessons/')
        data = r.json()
        self.assertEqual(len(data), 0)


class ResultViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = baker.make("Student")
        self.test_obj = baker.make("Test")

    def test_get_list(self):
        result = baker.make("Result", student=self.student, test=self.test_obj)
        r = self.client.get('/api/results/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(result.score, data[0]['score'])
        self.assertEqual(result.student, data[0]['student'])

    def test_get_single(self):
        result = baker.make("Result", student=self.student, test=self.test_obj)
        r = self.client.get(f'/api/results/{result.id}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['id'], result.id)
        self.assertEqual(data['score'], result.score)
        self.assertEqual(data['student'], result.student.id)

    def test_create_result(self):
        result_data = {
            "student": self.student.id,
            "test": self.test_obj.id,
            "score": 85,
            "date": "2023-10-01"
        }
        r = self.client.post('/api/results/', result_data, format='json')
        self.assertEqual(r.status_code, 201)
        
        data = r.json()
        self.assertEqual(data['student'], result_data['student'])
        self.assertEqual(data['test'], result_data['test'])
        self.assertEqual(data['score'], result_data['score'])

    def test_update_result(self):
        result = baker.make("Result", student=self.student, test=self.test_obj)
        update_data = {"score": 100}
        r = self.client.patch(f'/api/results/{result.id}/', update_data, format='json')
        self.assertEqual(r.status_code, 200)
        
        result.refresh_from_db()
        self.assertEqual(result.score, 100)

    def test_delete_result(self):
        result = baker.make("Result", student=self.student, test=self.test_obj)
        r = self.client.delete(f'/api/results/{result.id}/')
        self.assertEqual(r.status_code, 204)

        r = self.client.get('/api/results/')
        data = r.json()
        self.assertEqual(len(data), 0)