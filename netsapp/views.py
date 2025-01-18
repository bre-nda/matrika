from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Mattress, Duvet, Bedsheet, Pillow, CartItem
from django.shortcuts import redirect
from django.contrib import messages
import uuid

# Create your views here.

# def Home(request):
#     return render(request, 'index.html')

def Home(request):
    mattresses = Mattress.objects.all()
    duvets = Duvet.objects.all()
    bedsheets = Bedsheet.objects.all()
    pillows = Pillow.objects.all()
    
    return render(request, 'index.html', {
        'mattresses': mattresses,
        'duvets': duvets,
        'bedsheets': bedsheets,
        'pillows': pillows
    })
    


# Mattress Views
    
def mattress_page(request):
    mattresses = Mattress.objects.all()
    return render(request, 'mattress.html', {'mattresses': mattresses})

def quilted_mattress_page(request):
    quilted_mattresses = Mattress.objects.filter(type='quilted')  # Filter for quilted mattresses
    return render(request, 'quilted.html', {'quilted_mattresses': quilted_mattresses})

def plain_mattress_page(request):
    plain_mattresses = Mattress.objects.filter(type='plain')  #Filter for plain mattresses
    return render(request, 'plain.html', {'plain_mattresses': plain_mattresses})

def mattress_detail(request, type, thickness):
    size = request.GET.get('size')  # Get the selected size from the dropdown
    quantity = request.GET.get('quantity', 1)  # Get the selected quantity (default is 1)

    mattresses = Mattress.objects.filter(type=type, thickness=thickness)
    selected_mattress = None
    total_price = None

    if size:
        selected_mattress = mattresses.filter(size=size).first()  # Get the mattress for the selected size
        if selected_mattress:
            quantity = int(quantity)  # Convert to integer
            total_price = selected_mattress.price * quantity  # Calculate total price
            
            messages.success(request, "Your item has been added to the cart.")

    return render(request, 'mattress_detail.html', {
        'type': type,
        'thickness': thickness,
        'mattresses': mattresses,
        'selected_mattress': selected_mattress,
        'selected_size': size,
        'quantity': quantity,
        'total_price': total_price
    })
    
    
# Bedding views

def bedding_page(request):
    bedsheets = Bedsheet.objects.all()
    duvets = Duvet.objects.all()
    pillows = Pillow.objects.all()
    return render(request, 'bedding.html', {
        'bedsheets': bedsheets,
        'duvets': duvets,
        'pillows': pillows,
    })
    


# def pillow_detail(request, pk):
#     pillow = get_object_or_404(Pillow, id=pk)
#     selected_quantity = None
#     total_price = None

#     if request.method == "POST":
#         selected_quantity = int(request.POST.get('quantity', 1))  # Default quantity to 1 if not specified
#         total_price = pillow.price * selected_quantity

#     return render(request, 'pillow_detail.html', {
#         'pillow': pillow,
#         'selected_quantity': selected_quantity,
#         'total_price': total_price,
#     })
def pillow_detail(request, pk):
    pillow = get_object_or_404(Pillow, id=pk)
    selected_quantity = None
    total_price = None

    if request.method == "GET" and 'quantity' in request.GET:
        selected_quantity = int(request.GET.get('quantity', 1))  # Default quantity to 1 if not specified
        total_price = pillow.price * selected_quantity
        
        # Add success message
        messages.success(request, "Your item has been added to the cart.")

    return render(request, 'pillow_detail.html', {
        'pillow': pillow,
        'selected_quantity': selected_quantity,
        'total_price': total_price,
    })


def duvet_detail(request, pk):
    size = request.GET.get("size")
    color = request.GET.get("color")
    quantity = request.GET.get("quantity", 1)

    try:
        duvet = Duvet.objects.get(pk=pk)  # Get the specific duvet
        if size and color and duvet.size == size and duvet.color == color:
            total_price = float(duvet.price) * int(quantity)  # Calculate total price
        else:
            duvet = None
            total_price = None
    except Duvet.DoesNotExist:
        duvet = None
        total_price = None
        
        messages.success(request, "Your item has been added to the cart.")

    return render(request, 'duvet_detail.html', {
        'duvet': duvet,
        'size': size,
        'color': color,
        'quantity': quantity,
        'total_price': total_price,
    })
    

def bedsheet_detail(request, pk):
    size = request.GET.get("size")
    color = request.GET.get("color")
    quantity = request.GET.get("quantity", 1)

    try:
        bedsheet = Bedsheet.objects.get(pk=pk)  # Get the specific bedsheet
        if size and color and bedsheet.size == size and bedsheet.color == color:
            total_price = float(bedsheet.price) * int(quantity)  # Calculate total price
        else:
            bedsheet = None
            total_price = None
    except Bedsheet.DoesNotExist:
        bedsheet = None
        total_price = None
        
        messages.success(request, "Your item has been added to the cart.")

    return render(request, 'bedsheet_detail.html', {
        'bedsheet': bedsheet,
        'size': size,
        'color': color,
        'quantity': quantity,
        'total_price': total_price,
    })
    
# Add to cart
def add_to_cart(request, product_type, product_id):
    quantity = int(request.POST.get('quantity', 1))
    price = float(request.POST.get('price'))
    total_price = quantity * price
    

    if request.user.is_authenticated:
        # Save to database for logged-in users
        CartItem.objects.create(
            user=request.user,
            product_type=product_type,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
        )
    else:
        # Save to session for guests
        cart = request.session.get('cart', [])
        cart.append({
            'id': str(uuid.uuid4()),  # Unique ID for each item
            'product_type': product_type,
            'product_id': product_id,
            'quantity': quantity,
            'total_price': total_price,
        })
        request.session['cart'] = cart

    messages.success(request, "Item added to cart successfully.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

# cart page
# def cart_page(request):
#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(user=request.user)
#     else:
#         cart_items = request.session.get('cart', [])

#     return render(request, 'cart.html', {'cart_items': cart_items})
def cart_page(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id)

    return render(request, 'cart.html', {'cart_items': cart_items})

# delete cart
# def delete_cart_item(request, product_id, product_type):
#     if request.method == "POST":
#         cart = request.session.get('cart', [])
#         updated_cart = [
#             item for item in cart 
#             if not (item['product_id'] == product_id and item['product_type'] == product_type)
#         ]
#         request.session['cart'] = updated_cart
#         messages.success(request, "Item successfully removed from cart.")
#     return redirect('cart_page')

def delete_cart_item(request, cart_item_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Fetch the specific cart item by its unique ID
            cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
            cart_item.delete()
            messages.success(request, "Item successfully removed from your cart.")
        else:
            # Handle session-based cart for unauthenticated users
            cart = request.session.get('cart', [])
            updated_cart = [item for item in cart if item['id'] != cart_item_id]
            if len(cart) == len(updated_cart):
                messages.error(request, "Item not found in your cart.")
            else:
                messages.success(request, "Item successfully removed from your cart.")
            request.session['cart'] = updated_cart  # Update session cart

    return redirect('cart_page')

# def delete_cart_item(request, product_id, product_type):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             # Find all matching cart items for the user, product ID, and product type
#             cart_items = CartItem.objects.filter(
#                 user=request.user,
#                 product_id=product_id,
#                 product_type=product_type
#             )
#             if cart_items.exists():
#                 cart_items.delete()  # Delete all matching items
#                 messages.success(request, "Item(s) successfully removed from your cart.")
#             else:
#                 messages.error(request, "Item not found in your cart.")
#         else:
#             # Handle session-based cart for unauthenticated users
#             cart = request.session.get('cart', [])
#             updated_cart = [
#                 item for item in cart 
#                 if not (item['product_id'] == product_id and item['product_type'] == product_type)
#             ]
#             if len(cart) == len(updated_cart):
#                 messages.error(request, "Item not found in your cart.")
#             else:
#                 messages.success(request, "Item successfully removed from your cart.")
#             request.session['cart'] = updated_cart  # Update session cart

#     return redirect('cart_page')