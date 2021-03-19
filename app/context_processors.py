from .models import Category, Price, Score

def common(request):
    category_data = Category.objects.all()
    price_data = Price.objects.all()
    score_data = Score.objects.all()
    context = {
        'category_data': category_data,
        'price_data': price_data,
        'score_data': score_data,
    }
    return context
