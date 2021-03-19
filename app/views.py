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

	def post(self, request, *args, **kwargs):
		# 肌タイプのデータを取得
		dry_skintype_int = request.POST.getlist('skintype_dry')
		dry_len = len(dry_skintype_int)
		if dry_len == 0:
			return render(request, 'app/index.html')
		dry_skintype = int(dry_skintype_int[0])

		oil_skintype_int = request.POST.getlist('skintype_oil')
		oily_len = len(oil_skintype_int)
		if oily_len == 0:
			return render(request, 'app/index.html')
		oil_skintype = int(oil_skintype_int[0])

		skintype_data = []
		if dry_skintype >= 6 and oil_skintype >= 6:
			skintype_data.append("混合肌")
		elif dry_skintype <= 3 and oil_skintype <= 3:
			skintype_data.append("普通肌")
		elif dry_skintype > oil_skintype:
			skintype_data.append("乾燥肌")
		elif dry_skintype < oil_skintype:
			skintype_data.append("脂性肌")
		skintype_data = skintype_data[0]	

		# アイテムの種類を１種類ずつ
		wash_item = "洗顔"
		toner_item = "化粧水"
		cream_item = "乳液・クリーム"
		sunscreen_item = "日焼け止め"

		# プライスのデータ取得
		checked_price = request.POST.getlist('price')
		price_len = len(checked_price)
		if price_len == 0:
			return render(request, 'app/index.html')
		price = int(checked_price[0])

		# 悩みのデータ取得
		checked_trouble_data = request.POST.getlist('trouble')
		if checked_trouble_data == ['']:
			recommend_data = Recommenditem.objects.all().filter(skintype=skintype_data).filter(price_data=price)
			wash_recommend_data = recommend_data.filter(item=wash_item)
			toner_recommend_data = recommend_data.filter(item=toner_item)
			cream_recommend_data = recommend_data.filter(item=cream_item)
			sunscreen_recommend_data = recommend_data.filter(item=sunscreen_item)

			if wash_recommend_data:
				wash_recommend_data = wash_recommend_data[0]
			if toner_recommend_data:
				toner_recommend_data = toner_recommend_data[0]
			if cream_recommend_data:
				cream_recommend_data = cream_recommend_data[0]
			if sunscreen_recommend_data:
				sunscreen_recommend_data = sunscreen_recommend_data[0]

			if skintype_data =='混合肌':
				file_template = 'app/mixskin.html'
			elif skintype_data == '普通肌':
				file_template = 'app/normalskin.html'
			elif skintype_data == '脂性肌':
				file_template = 'app/oilyskin.html'
			elif skintype_data == '乾燥肌':
				file_template = 'app/dryskin.html'
			else:
				file_template = 'app/index.html'
			return render(request, file_template, {
				'wash_recommend_data': wash_recommend_data,
				'toner_recommend_data': toner_recommend_data,
				'cream_recommend_data': cream_recommend_data,
				'sunscreen_recommend_data': sunscreen_recommend_data,
			})


		checked_trouble = checked_trouble_data[0]
		checked = checked_trouble.split(',')
		checked_len = len(checked)
		trouble_il = []
		check_il =[]
		for i in range(checked_len):
			x = int(checked[i])
			if x == 0:
				trouble_il.append("wrinkle_point")
				check_il.append("trouble_name3")
			elif x == 1:
				trouble_il.append("spots_point")
				check_il.append("trouble_name4")
			elif x == 2:
				trouble_il.append("pores_point")
				check_il.append("trouble_name2")
			elif x == 3:
				trouble_il.append("acne_point")
				check_il.append("trouble_name1")

		if checked_len == 4:
			trouble1 = trouble_il[0]
			trouble2 = trouble_il[1]

			recommend_data = Recommenditem.objects.order_by(trouble1).filter(skintype=skintype_data).filter(price_data=price)

			recommend_data_acne = recommend_data.filter(trouble_name1='ニキビ')
			recommend_data_pore = recommend_data.filter(trouble_name2='毛穴')
			recommend_data_linkle = recommend_data.filter(trouble_name3='シワ')
			recommend_data_spots = recommend_data.filter(trouble_name4='髭剃り負け')

			for i in check_il:
				if i == "trouble_name1":
					recommend_data = recommend_data_acne
				elif i == "trouble_name2":
					recommend_data = recommend_data_pore
				elif i == "trouble_name3":
					recommend_data = recommend_data_linkle
				else:
					recommend_data = recommend_data_spots

			recommend_data = recommend_data.order_by(trouble2)
			
			wash_recommend_data = recommend_data.filter(item=wash_item)
			toner_recommend_data = recommend_data.filter(item=toner_item)
			cream_recommend_data = recommend_data.filter(item=cream_item)
			sunscreen_recommend_data = recommend_data.filter(item=sunscreen_item)

			if wash_recommend_data:
				wash_recommend_data = wash_recommend_data[0]
			if toner_recommend_data:
				toner_recommend_data = toner_recommend_data[0]
			if cream_recommend_data:
				cream_recommend_data = cream_recommend_data[0]
			if sunscreen_recommend_data:
				sunscreen_recommend_data = sunscreen_recommend_data[0]

			if skintype_data =='混合肌':
				file_template = 'app/mixskin.html'
			elif skintype_data == '普通肌':
				file_template = 'app/normalskin.html'
			elif skintype_data == '脂性肌':
				file_template = 'app/oilyskin.html'
			elif skintype_data == '乾燥肌':
				file_template = 'app/dryskin.html'
			else:
				file_template = 'app/index.html'
			return render(request, file_template, {
				'wash_recommend_data': wash_recommend_data,
				'toner_recommend_data': toner_recommend_data,
				'cream_recommend_data': cream_recommend_data,
				'sunscreen_recommend_data': sunscreen_recommend_data,
			})
			
		elif checked_len == 3:
			trouble1 = trouble_il[0]
			trouble2 = trouble_il[1]

			recommend_data = Recommenditem.objects.order_by(trouble1).filter(skintype=skintype_data).filter(price_data=price)
			recommend_data_acne = recommend_data.filter(trouble_name1='ニキビ')
			recommend_data_pore = recommend_data.filter(trouble_name2='毛穴')
			recommend_data_linkle = recommend_data.filter(trouble_name3='シワ')
			recommend_data_spots = recommend_data.filter(trouble_name4='髭剃り負け')

			for i in check_il:
				if i == "trouble_name1":
					recommend_data = recommend_data_acne
				elif i == "trouble_name2":
					recommend_data = recommend_data_pore
				elif i == "trouble_name3":
					recommend_data = recommend_data_linkle
				else:
					recommend_data = recommend_data_spots

			recommend_data = recommend_data.order_by(trouble2)
			
			wash_recommend_data = recommend_data.filter(item=wash_item)
			toner_recommend_data = recommend_data.filter(item=toner_item)
			cream_recommend_data = recommend_data.filter(item=cream_item)
			sunscreen_recommend_data = recommend_data.filter(item=sunscreen_item)

			if wash_recommend_data:
				wash_recommend_data = wash_recommend_data[0]
			if toner_recommend_data:
				toner_recommend_data = toner_recommend_data[0]
			if cream_recommend_data:
				cream_recommend_data = cream_recommend_data[0]
			if sunscreen_recommend_data:
				sunscreen_recommend_data = sunscreen_recommend_data[0]

			if skintype_data =='混合肌':
				file_template = 'app/mixskin.html'
			elif skintype_data == '普通肌':
				file_template = 'app/normalskin.html'
			elif skintype_data == '脂性肌':
				file_template = 'app/oilyskin.html'
			elif skintype_data == '乾燥肌':
				file_template = 'app/dryskin.html'
			else:
				file_template = 'app/index.html'
			return render(request, file_template, {
				'wash_recommend_data': wash_recommend_data,
				'toner_recommend_data': toner_recommend_data,
				'cream_recommend_data': cream_recommend_data,
				'sunscreen_recommend_data': sunscreen_recommend_data,
			})

		elif checked_len == 2:
			trouble1 = trouble_il[0]

			recommend_data = Recommenditem.objects.order_by(trouble1).filter(skintype=skintype_data).filter(price_data=price)
			recommend_data_acne = recommend_data.filter(trouble_name1='ニキビ')
			recommend_data_pore = recommend_data.filter(trouble_name2='毛穴')
			recommend_data_linkle = recommend_data.filter(trouble_name3='シワ')
			recommend_data_spots = recommend_data.filter(trouble_name4='髭剃り負け')

			for i in check_il:
				if i == "trouble_name1":
					recommend_data = recommend_data_acne
				elif i == "trouble_name2":
					recommend_data = recommend_data_pore
				elif i == "trouble_name3":
					recommend_data = recommend_data_linkle
				else:
					recommend_data = recommend_data_spots
				
			wash_recommend_data = recommend_data.filter(item=wash_item)
			toner_recommend_data = recommend_data.filter(item=toner_item)
			cream_recommend_data = recommend_data.filter(item=cream_item)
			sunscreen_recommend_data = recommend_data.filter(item=sunscreen_item)

			if wash_recommend_data:
				wash_recommend_data = wash_recommend_data[0]
			if toner_recommend_data:
				toner_recommend_data = toner_recommend_data[0]
			if cream_recommend_data:
				cream_recommend_data = cream_recommend_data[0]
			if sunscreen_recommend_data:
				sunscreen_recommend_data = sunscreen_recommend_data[0]

			if skintype_data =='混合肌':
				file_template = 'app/mixskin.html'
			elif skintype_data == '普通肌':
				file_template = 'app/normalskin.html'
			elif skintype_data == '脂性肌':
				file_template = 'app/oilyskin.html'
			elif skintype_data == '乾燥肌':
				file_template = 'app/dryskin.html'
			else:
				file_template = 'app/index.html'
			return render(request, file_template, {
				'wash_recommend_data': wash_recommend_data,
				'toner_recommend_data': toner_recommend_data,
				'cream_recommend_data': cream_recommend_data,
				'sunscreen_recommend_data': sunscreen_recommend_data,
			})


		elif checked_len == 1:
			trouble1 = trouble_il[0]

			recommend_data = Recommenditem.objects.order_by(trouble1).filter(skintype=skintype_data).filter(price_data=price)
			recommend_data_acne = recommend_data.filter(trouble_name1='ニキビ')
			recommend_data_pore = recommend_data.filter(trouble_name2='毛穴')
			recommend_data_linkle = recommend_data.filter(trouble_name3='シワ')
			recommend_data_spots = recommend_data.filter(trouble_name4='髭剃り負け')

			for i in check_il:
				if i == "trouble_name1":
					recommend_data = recommend_data_acne
				elif i == "trouble_name2":
					recommend_data = recommend_data_pore
				elif i == "trouble_name3":
					recommend_data = recommend_data_linkle
				else:
					recommend_data = recommend_data_spots
				
			wash_recommend_data = recommend_data.filter(item=wash_item)
			toner_recommend_data = recommend_data.filter(item=toner_item)
			cream_recommend_data = recommend_data.filter(item=cream_item)
			sunscreen_recommend_data = recommend_data.filter(item=sunscreen_item)

			if wash_recommend_data:
				wash_recommend_data = wash_recommend_data[0]
			if toner_recommend_data:
				toner_recommend_data = toner_recommend_data[0]
			if cream_recommend_data:
				cream_recommend_data = cream_recommend_data[0]
			if sunscreen_recommend_data:
				sunscreen_recommend_data = sunscreen_recommend_data[0]

			if skintype_data =='混合肌':
				file_template = 'app/mixskin.html'
			elif skintype_data == '普通肌':
				file_template = 'app/normalskin.html'
			elif skintype_data == '脂性肌':
				file_template = 'app/oilyskin.html'
			elif skintype_data == '乾燥肌':
				file_template = 'app/dryskin.html'
			else:
				file_template = 'app/index.html'
			return render(request, file_template, {
				'wash_recommend_data': wash_recommend_data,
				'toner_recommend_data': toner_recommend_data,
				'cream_recommend_data': cream_recommend_data,
				'sunscreen_recommend_data': sunscreen_recommend_data,
			})


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


class ReviewDetailView(View):
	def get(self, request, *args, **kwargs):
		#review全件
		review = Review.objects.all()
		# 詳細のデータ
		review_data = review.get(id=self.kwargs['pk'])
		#詳細のデータのユーザー
		detail_user = review_data.user
		user_count = review.filter(user=detail_user).count()
		#自分のプロフィール
		user_data = CustomUser.objects.get(id=request.user.id)
		#自分が投稿したreviewの件数
		user_review = review.filter(user=user_data)
		count = user_review.count()
		#自分が投稿したreviewの最新
		new_review = user_review.order_by('-id')
		if new_review:
			new_review = new_review[0]
		#review全体の中から最新のもの
		all_review_new = review.order_by('-id')
		new_data = all_review_new[0]

		form = ReviewForm(request.POST or None)

		return render(request, 'app/review_detail.html', {
			'user_count':user_count,
			'new_data':new_data,
			'count':count,
			'form': form,
			'user_data': user_data,
			'review_data': review_data,
			'new_review':new_review,
			})


class CreateReviewView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		#クチコミ全件取得
		review= Review.objects.order_by('-id')
		#ユーザーデータの取得
		user_data = CustomUser.objects.get(id=request.user.id)
		#クチコミからユーザーのもののみ取得
		user_review = review.filter(user=user_data)
		#ユーザーのクチコミ件数取得
		count = user_review.count()
		#全部のクチコミから新しいもの1件
		if review:
			review = review[0]
		#ユーザーのクチコミ最新
		if user_review:
			user_review = user_review[0]

		form = ReviewForm(request.POST or None)

		return render(request, 'app/review_form.html', {
			'review':review,
			'user_review':user_review,
			'count':count,
			'form': form,
			'user_data': user_data,
			})

	def post(self, request, *args, **kwargs):
		form = ReviewForm(request.POST or None)

		if form.is_valid():
			review_data = Review()
			review_data.user = request.user
			review_data.brand = form.cleaned_data['brand']
			review_data.product = form.cleaned_data['product']
			category = form.cleaned_data['category']
			category_data = Category.objects.get(name=category)
			review_data.category = category_data
			price = form.cleaned_data['price']
			price_data = Price.objects.get(price=price)
			review_data.price = price_data
			score = form.cleaned_data['score']
			score_data = Score.objects.get(scores=score)
			review_data.score = score_data
			review_data.comment = form.cleaned_data['comment']
			if request.FILES:
				review_data.image = request.FILES.get('image')
			review_data.save()
			return redirect('review_detail', review_data.id)

		return render(request, 'app/review_form.html', {
			'form': form
		})


class ReviewEditView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		user_data = CustomUser.objects.get(id=request.user.id)
		count = Review.objects.filter(user=user_data).count()
		new_review = Review.objects.filter(user=user_data).order_by('-id')

		if new_review:
			new_review = new_review[0]

		new = new_review
		all_review_new = Review.objects.order_by('-id')
		new_data = all_review_new[0]

		review_data = Review.objects.get(id=self.kwargs['pk'])
		form = ReviewForm(
			request.POST or None,
			initial={
				'brand': review_data.brand,
				'product': review_data.product,
				'category': review_data.category,
				'price': review_data.price,
				'score': review_data.score,
				'comment': review_data.comment,
				'image': review_data.image,
			}
		)

		return render(request, 'app/review_edit.html', {
			'form': form,
			'new_data':new_data,
			'new':new,
			'count':count,
			'form': form,
			'user_data': user_data,
		})

	
	def post(self, request, *args, **kwargs):
		form = ReviewForm(request.POST or None)

		if form.is_valid():
			review_data = Review.objects.get(id=self.kwargs['pk'])
			review_data.brand = form.cleaned_data['brand']
			review_data.product = form.cleaned_data['product']
			category = form.cleaned_data['category']
			category_data = Category.objects.get(name=category)
			review_data.category = category_data
			price = form.cleaned_data['price']
			price_data = Price.objects.get(price=price)
			review_data.price = price_data
			score = form.cleaned_data['score']
			score_data = Score.objects.get(scores=score)
			review_data.score = score_data
			review_data.comment = form.cleaned_data['comment']
			if request.FILES:
				review_data.image = request.FILES.get('image')
			review_data.save()
			return redirect('review_detail', self.kwargs['pk'])

		return render(request, 'app/review_form.html', {
			'form': form
		})


class ReviewDeleteView(View):
	def get(self, request, *args, **kwargs):
		#削除するreview
		review_data = Review.objects.get(id=self.kwargs['pk'])
		#本人ユーザーデータ名
		user_data = CustomUser.objects.get(id=request.user.id)
		#本人ユーザーのreview件数
		user_review =  Review.objects.filter(user=user_data)
		count = user_review.count()
		#本人ユーザーの最新クチコミ
		new_review = user_review.order_by('-id')
		if new_review:
			new＿review = new_review[0]
		#全てのreviewから最新のもの	
		all_review_new = Review.objects.order_by('-id')
		new_data = all_review_new[0]

		form = ReviewForm(request.POST or None)

		return render(request, 'app/review_delete.html', {
			'new_data':new_data,
			'new_review':new_review,
			'count':count,
			'form': form,
			'user_data': user_data,
			'review_data': review_data
			})

	def post(self, request, *args, **kwargs):
		review_data = Review.objects.get(id=self.kwargs['pk'])
		review_data.delete()
		return redirect('myreview_list')


class MyReviewListView(LoginRequiredMixin,View):
	def get(self, request, *args, **kwargs):
		#クチコミ全件取得
		review= Review.objects.order_by('-id')
		#ユーザーデータの取得
		user_data = CustomUser.objects.get(id=request.user.id)
		#クチコミからユーザーのもののみ取得
		user_review = review.filter(user=user_data)
		#ユーザーのクチコミ件数取得
		count = user_review.count()
		#1ページに出す件数
		paginator = Paginator(user_review, 5)
		#現在のページ
		page = request.GET.get('page')
		#10件のreview
		all_review = paginator.get_page(page)
		#全部のクチコミから新しいもの1件
		if review:
			review = review[0]
		#ユーザーのクチコミ最新
		if user_review:
			user_review = user_review[0]

		return render(request, 'app/myreview_list.html', {
			'user_data': user_data,
			'count':count,
			'review':review,
			'all_review': all_review
		})


class CategoryView(View):
	def get(self, request, *args, **kwargs):
		#全てのreview
		review = Review.objects.order_by('-id')
		#カテゴリーでフィルター
		category_name = Category.objects.get(name=self.kwargs['category'])
		#全てのreviewからフィルターしたものの件数
		total_count = review.filter(category=category_name).count()
		#1ページに出す件数
		paginator = Paginator(review.filter(category=category_name), 10)
		#ページ数をゲット
		page = request.GET.get('page')
		#
		all_review = paginator.get_page(page)

		return render(request, 'app/review.html', {
			'category_name':category_name,
			'all_review': all_review,
			'total_count':total_count,
		})


class PriceView(View):
	def get(self, request, *args, **kwargs):
		#全てのreview
		review = Review.objects.order_by('-id')
		#カテゴリーでフィルター
		category_name = Price.objects.get(price=self.kwargs['price'])
		#全てのreviewからフィルターしたものの件数
		total_count = review.filter(price=category_name).count()
		#1ページに出す件数
		paginator = Paginator(review.filter(price=category_name), 10)
		#ページ数をゲット
		page = request.GET.get('page')
		#
		all_review = paginator.get_page(page)

		return render(request, 'app/review.html', {
			'category_name':category_name,
			'all_review': all_review,
			'total_count':total_count,
		})


class ScoreView(View):
	def get(self, request, *args, **kwargs):
		#全てのreview
		review = Review.objects.order_by('-id')
		#カテゴリーでフィルター
		category_name = Score.objects.get(scores=self.kwargs['score'])
		#全てのreviewからフィルターしたものの件数
		total_count = review.filter(score=category_name).count()
		#1ページに出す件数
		paginator = Paginator(review.filter(score=category_name), 10)
		#ページ数をゲット
		page = request.GET.get('page')
		#
		all_review = paginator.get_page(page)

		return render(request, 'app/review.html', {
			'category_name':category_name,
			'all_review': all_review,
			'total_count':total_count,
		})



class SearchView(View):
	def get(self, request, *args, **kwargs):
		#全てのreview
		review_data = Review.objects.order_by('-id')
		#キーワード取得
		keyword = request.GET.get('keyword')


		query_il = []

		if keyword:
			exclusion_list = set([' ', '　'])
			query_list = ''
			for word in keyword:
				if not word in exclusion_list:
					query_list += word
			query = reduce(and_, [Q(brand__icontains=q) | Q(comment__icontains=q) for q in query_list])
			query_il.append(reduce(and_, [Q(brand__icontains=q) | Q(comment__icontains=q) for q in query_list]))
			all_review = review_data.filter(query)
			#検索でヒットした件数
			total_count = all_review.count()

		return render(request, 'app/review.html', {
			'keyword': keyword,
			'all_review': all_review,
			'total_count':total_count,
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