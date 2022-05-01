from django.test import TestCase
from django.shortcuts import resolve_url as resolve
# Create your tests here.


class HomeTest(TestCase):

    def setUp(self) -> None:
        self.response = self.client.get(resolve('home'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use template index.html"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        expected = 'href="{}"'.format(resolve('subscriptions:new'))
        self.assertContains(self.response, 'href="/inscricao/"')
        # self.assertContains(self.response, 'href="/inscricao/"')

    def test_speakers(self):
        """"Must show keynote speakers"""
        contents = [
            'Grace Hopper',
            'http://hbn.link/hopper-pic',
            'Alan Turing',
            'http://hbn.link/turing-pic'
        ]

        for expect in contents:
            with self.subTest():
                self.assertContains(self.response, expect)

    def test_speakers_link(self):
        expect = 'href="{}#speakers"'.format(resolve('home'))
        self.assertContains(self.response, expect)
