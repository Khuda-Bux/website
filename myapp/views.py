from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer,Product,Cart,OrderPlaced
from .forms import MyCustomer
from django.contrib import messages
# Create your views here.
###########address custmer
def show_address(request):
    if request.method == 'POST':
        fm = MyCustomer(request.POST)
        if fm.is_valid():
           
            # Set the user for the Customer object
            customer = fm.save(commit=False)
            customer.user = request.user  # Assuming the user is authenticated
            customer.save()
            messages.success(request,' Congratulations Your Form have been submit successfuly!!') 
        fm = MyCustomer()   
    else:
        fm = MyCustomer()
    return render(request, 'myapp/address.html', {'form': fm})



def show_product(request):
    fm=Product.objects.all()
    return render(request, 'myapp/home.html',{'form':fm})


def show_category(request):
    category = request.GET.get('category', 'C')  # Default to 'c' if category parameter not provided
    products = Product.objects.filter(category__iexact=category)
    return render(request, 'myapp/category.html', {'products': products})

def detail_item(request, id):
    product_id=get_object_or_404(Product,pk=id)
    context={'x':product_id}
    return render(request, 'myapp/detail.html',context)

## add cart
def add_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        #print('cart_ides add cart',prod_id)
        if prod_id:
            cart_items = request.session.get('cart_items', [])
            cart_items.append(prod_id)
            request.session['cart_items'] = cart_items
    cart_items = request.session.get('cart_items', [])
    products_in_cart = Product.objects.filter(pk__in=cart_items)
    return render(request, 'myapp/add_cart.html', {'cart_items': products_in_cart})

##delete cart
def delete_cart(request):
    if request.method == 'POST':
        request.session.pop('cart_items', None)
    return redirect('add_cart')  # Assuming 'cart' is the name of the URL/view for your cart page
################ search item
def product_search(request):
    
    query = request.GET.get('q')
    products = []

    if query:
        products = Product.objects.filter(brand__icontains=query)
    return render(request, 'myapp/searching.html', {'products': products})
    

