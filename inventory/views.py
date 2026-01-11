from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Sum, Min, Max, F, Case, When, Value, CharField
from django.db.models.functions import TruncMonth
from .models import Product, Sale
from .forms import ProductForm
import json
import csv
from django.contrib.auth.models import User
from datetime import date

# ---------------------------------------------------------
# MAIN DASHBOARD VIEW
# ---------------------------------------------------------
def dashboard(request):
    total_products = Product.objects.count()
    total_sales_records = Sale.objects.count()
    sales_data = Sale.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('total_amount')).order_by('month')
    labels_trend = [item['month'].strftime('%b-%Y') for item in sales_data]
    data_trend = [float(item['total']) for item in sales_data]
    cat_data = Sale.objects.values('product_category').annotate(qty=Sum('quantity')).order_by('-qty')[:5]
    labels_cat = [item['product_category'] for item in cat_data]
    data_cat = [item['qty'] for item in cat_data]
    total_revenue = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_stock = Product.objects.aggregate(Sum('inventory_level'))['inventory_level__sum'] or 0
    low_stock_count = Product.objects.filter(inventory_level__lt=20).count()

    context = {
        'labels_trend': json.dumps(labels_trend), 'data_trend': json.dumps(data_trend),
        'labels_cat': json.dumps(labels_cat), 'data_cat': json.dumps(data_cat),
        'total_revenue': round(total_revenue, 2), 'total_stock': total_stock,
        'low_stock_count': low_stock_count,
    }
    return render(request, 'index.html', context)

# ---------------------------------------------------------
# INVENTORY VIEWS
# ---------------------------------------------------------
def Inventory(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'Inventory.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Inventory')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Inventory')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('Inventory')

# ---------------------------------------------------------
# OTHER PAGES VIEWS
# ---------------------------------------------------------
def Sales(request):
    sales = Sale.objects.all()
    context = {'sales': sales}
    return render(request, 'Sales.html', context)

def DemandForecasting(request):
    category_sales = Sale.objects.values('product_category').annotate(total_sold=Sum('quantity'))
    category_stock = Product.objects.values('category').annotate(current_stock=Sum('inventory_level'))
    sales_dates = Sale.objects.aggregate(min_date=Min('date'), max_date=Max('date'))
    min_date, max_date = sales_dates.get('min_date'), sales_dates.get('max_date')
    
    total_months = 1
    if min_date and max_date:
        total_months = (max_date.year - min_date.year) * 12 + max_date.month - min_date.month + 1
        total_months = max(1, total_months)

    forecasting_data = []
    for sale in category_sales:
        category = sale['product_category']
        stock_info = next((s for s in category_stock if s['category'] == category), {'current_stock': 0})
        avg_monthly_sales = sale['total_sold'] / total_months
        forecasting_data.append({
            'category': category,
            'current_stock': stock_info['current_stock'],
            'total_sold': sale['total_sold'],
            'predicted_demand': int(avg_monthly_sales * 1.10)
        })

    context = {
        'forecasting_data': forecasting_data,
        'chart_labels': json.dumps([d['category'] for d in forecasting_data]),
        'chart_total_sold': json.dumps([d['total_sold'] for d in forecasting_data]),
        'chart_predicted_demand': json.dumps([d['predicted_demand'] for d in forecasting_data])
    }
    return render(request, 'DemandForecasting.html', context)

def PurchasePlan(request):
    purchase_plan_data = Product.objects.filter(inventory_level__lt=20).annotate(
        required_quantity=50 - F('inventory_level'),
        status=Case(When(inventory_level=0, then=Value('Critical')), default=Value('Warning'), output_field=CharField())
    )
    context = {'purchase_plan_data': purchase_plan_data}
    return render(request, 'PurchasePlan.html', context)

def SmartAlerts(request):
    out_of_stock_products = Product.objects.filter(inventory_level=0)
    low_stock_products = Product.objects.filter(inventory_level__gt=0, inventory_level__lt=20)
    context = {
        'out_of_stock_products': out_of_stock_products, 'low_stock_products': low_stock_products,
        'out_of_stock_count': out_of_stock_products.count(), 'low_stock_count': low_stock_products.count(),
    }
    return render(request, 'SmartAlerts.html', context)

def DownloadReports(request):
     return render(request,'DownloadReports.html')

# ---------------------------------------------------------
# DOWNLOAD VIEWS
# ---------------------------------------------------------
def download_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Transaction ID', 'Date', 'Product Category', 'Quantity', 'Total Amount'])
    
    sales = Sale.objects.all().values_list('transaction_id', 'date', 'product_category', 'quantity', 'total_amount')
    for sale in sales:
        writer.writerow(sale)
        
    return response

def download_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Product ID', 'Product Name', 'Category', 'Inventory Level', 'Cost Price'])
    
    products = Product.objects.all().values_list('product_id', 'name', 'category', 'inventory_level', 'cost_price')
    for product in products:
        writer.writerow(product)
        
    return response
