from django.urls import path
from app import views

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('dryskin/', views.DryskinView.as_view(), name='dryskin'),
	path('oilyskin/', views.OilyskinView.as_view(), name='oilyskin'),
	path('mixskin/', views.MixskinView.as_view(), name='mixskin'),
	path('normal/', views.NormalskinView.as_view(), name='normalskin'),
	path('skin_feature/', views.SkinFeatureView.as_view(), name='skin_feature'),
	path('review/', views.ReviewView.as_view(), name='review'),
	path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
	path('review/new/', views.CreateReviewView.as_view(), name='review_new'),
	path('review/<int:pk>/edit/', views.ReviewEditView.as_view(), name='review_edit'),
	path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
	path('myreviewlist/', views.MyReviewListView.as_view(), name='myreview_list'),
	path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
	path('price/<str:price>/', views.PriceView.as_view(), name='price'),
	path('score/<str:score>/', views.ScoreView.as_view(), name='score'),
	path('search/', views.SearchView.as_view(), name='search'),
	path('contact/', views.ContactView.as_view(), name='contact'),
	path('thanks/', views.ThanksView.as_view(), name='thanks'),
]