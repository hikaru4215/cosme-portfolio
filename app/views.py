from django.shortcuts import render, redirect
from django.views.generic import View
# from .models import Recommenditem, Review, Category, Price, Score
# from .forms import ContactForm, ReviewForm
# from django.conf import settings
# from django.http import HttpResponse, JsonResponse
# from django.core.mail import BadHeaderError, EmailMessage, send_mail
# from django.contrib.auth.mixins import LoginRequiredMixin
# from accounts.models import CustomUser
# from django.db.models import Q, Avg
# from functools import reduce
# from operator import and_
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
# import textwrap, re

class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/index.html')