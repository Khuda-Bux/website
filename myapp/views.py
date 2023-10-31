from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from .models import Customer,Product,Cart,OrderPlaced
from .forms import MyCustomer,My_Cart
from django.contrib import messages
from .forms import Registrationform
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, login, logout
# Create your views here.
###########address custmer
##login AuthenticationForm
def login_page(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        fm = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': fm}) 
#registrationform user
def Reg(request):
    if request.method=='POST':
     fm=Registrationform(request.POST)
     if fm.is_valid():
         fm.save()
         messages.success(request, 'You Registration Successfuly Thanx!!') 
    else:
        fm=Registrationform()
    return render(request, 'myapp/reg.html',{'form':fm})


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
    fm=My_Cart()
    context={'x':product_id,'form':fm}
    return render(request, 'myapp/detail.html',context)

def cart_detail(request):
    fm=My_Cart()
    return render(request,'myapp/cartdetail.html',{'form':fm})

## add cart
# def add_cart(request):
#     if request.method == 'POST':
#         prod_id = request.POST.get('prod_id')
#         #print('cart_ides add cart',prod_id)
#         if prod_id:
#             cart_items = request.session.get('cart_items', [])
#             cart_items.append(prod_id)
#             request.session['cart_items'] = cart_items
#     cart_items = request.session.get('cart_items', [])
#     products_in_cart = Product.objects.filter(pk__in=cart_items)
#     if request.method=='POST': 
#      fm=My_Cart(request.POST)
#     if fm.is_valid():
#         fm.save()
#     else:
#         My_Cart()
#     return render(request, 'myapp/add_cart.html', {'cart_items': products_in_cart,'form':fm})
#custom code
# Add an item to the cart
# def add_cart(request):
#     if request.method == 'POST':
#      prod_id =request.POST.get('prod_id')
#      request.session['prod_id'] = prod_id
#      cart_item = request.session['prod_id']     
#      print('my dear this this prod yes it',cart_item)
#      products_in_cart = Product.objects.filter(pk__in=cart_item)
#      print('filter my value kb=',products_in_cart)
#      return render(request, 'myapp/add_cart.html', {'cart_items':products_in_cart})


def add_cart(request):
        user = request.user
        product_id = request.GET.get('prod_id')
        # Get the Product instance using the product_id
        product = get_object_or_404(Product, id=product_id)
        # Create a Cart instance with the user and product, then save it
        cart = Cart(user=user, product=product)
        cart.save()
        return redirect('/cart')
def show_cart(request):
    cart = None  # Initialize cart as None or an empty list as a default value
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0  # Define a default value here
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                
    return render(request, 'myapp/add_cart.html', {'cart': cart, 'totalamount': totalamount, 'amount': amount})







def cart_detail(request):
    fm=Cart.objects.values('quantity')
    print('Show dictionery values',fm)
    print()
    fm2=Product.objects.values('selling_price')
    print('Show dictionery values',fm2)


    return render(request, 'myapp/cartdetail.html',{'form':fm,'form2':fm2})


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
    

