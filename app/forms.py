from django import forms
from .models import Review, Category, Price, Score


class ReviewForm(forms.Form):
	category_data = Category.objects.all()
	category_choice = {}
	for category in category_data:
		category_choice[category] = category


	price_data = Price.objects.all()
	price_choice = {}
	for price in price_data:
		price_choice[price] = price

	score_data = Score.objects.all()
	score_choice = {}
	for score in score_data:
		score_choice[score] = score


	brand = forms.CharField(label="ブランド名", max_length=100, required=False)
	product = forms.CharField(label="製品名", max_length=100)
	category = forms.ChoiceField(label='カテゴリ', widget=forms.Select, choices=list(category_choice.items()))
	price = forms.ChoiceField(label="プライス", widget=forms.Select, choices=list(price_choice.items()), required=False)
	score = forms.ChoiceField(label="おすすめ度", widget=forms.Select, choices=list(score_choice.items()))
	comment = forms.CharField(label="クチコミ", widget=forms.Textarea())
	image = forms.ImageField(label='イメージ画像', required=False)
	review_count = forms.CharField(label='クチコミ件数', max_length=100, required=False)



class ContactForm(forms.Form):
	name = forms.CharField(max_length=50, label='名前')
	email = forms.EmailField(max_length=50, label='メールアドレス')
	content = forms.CharField(label='クチコミ', widget=forms.Textarea())

