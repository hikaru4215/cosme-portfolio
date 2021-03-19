from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Recommenditem, Review, Category, Price, Score
from .forms import ContactForm, ReviewForm
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from django.db.models import Q, Avg
from functools import reduce
from operator import and_
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
import textwrap, re

class IndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/index.html')

class DryskinView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/dryskin.html')

class OilyskinView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/oilyskin.html')

class NormalskinView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/normalskin.html')

class MixskinView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/mixskin.html')


class SkinFeatureView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/skin_feature.html')

class ReviewView(LoginRequiredMixin,View):
	def get(self, request, *args, **kwargs):
		# 全てのreview
		review = Review.objects.order_by('-id')
		#全てのreview件数
		total_count = review.count()
		#1ページに出す件数
		paginator = Paginator(review, 10)
		#現在のページ
		page = request.GET.get('page')
		#10件のreview
		all_review = paginator.get_page(page)

		return render(request, 'app/review.html', {
			'total_count': total_count,
			'all_review': all_review
			})

class ContactView(View):
	def get(self, request, *args, **kwargs):
		form = ContactForm(request.POST or None)

		return render(request, 'app/contact.html', {
			'form': form
		})


	def post(self, request, *args, **kwargs):
		form = ContactForm(request.POST or None)

		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			content = form.cleaned_data['content']

			if re.search('[ぁ-ん]', content) == None:
				return redirect('thanks')

			if re.search('https://', contact) == None:
				return redirect('thanks')

			subject = 'お問い合わせありがとうございます。'
			message = textwrap.dedent('''
				※このメールはシステムからの自動返信です。
                
                {name} 様
                
                お問い合わせありがとうございました。
                以下の内容でお問い合わせを受け付けいたしました。
                内容を確認させていただき、ご返信させて頂きますので、少々お待ちください。
                
                --------------------
                ■お名前
                {name}
                
                ■メールアドレス
                {email}
                
                ■メッセージ
                {content}
                --------------------
                ''').format(
					name=name,
					email=email,
					content=content
				)

			to_list = [email]
			bcc_list = [settings.EMAIL_HOST_USER]

			try:
				message = EmailMessage(subject=subject, body=message, to=to_list, bcc=bcc_list)
				message.send()
			except BadHeaderError:
				return HttpResponse("無効なヘッダが検出されました。")

			return redirect('thanks')

		return render(request, 'app/contact.html', {
			'form':form
		})

class ThanksView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'app/thanks.html')