from django.test import TestCase
from LearnModels import models as learn_models
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

test_cat = learn_models.Category()
learn_models.Category.objects.get()
