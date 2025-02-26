from decimal import Decimal
import re
from unittest import result
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, UserProfile, ShippingAddress, BillingAddress
from .forms import UserProfileForm,ShippingAddressForm, BillingAddressForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from .models import Mattress, Duvet, Bedsheet, Pillow, CartItem
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.db.models import Q

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.apps import apps
from uuid import uuid4  # Import UUID to generate unique keys


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
# def add_to_cart(request, product_type, product_id):
#     quantity = int(request.POST.get('quantity', 1))
#     price = float(request.POST.get('price'))
#     total_price = quantity * price

#     if request.user.is_authenticated:
#         # Save to database for logged-in users
#         CartItem.objects.create(
#             user=request.user,
#             product_type=product_type,
#             product_id=product_id,
#             quantity=quantity,
#             total_price=total_price,
#         )
#     else:
#         # Ensure session is created for guest users
#         if not request.session.session_key:
#             request.session.create()

#         cart = request.session.get('cart', [])

#         # Add item to session cart
#         cart.append({
#             'id': str(uuid.uuid4()),  # Unique ID for each item
#             'product_type': product_type,
#             'product_id': product_id,
#             'quantity': quantity,
#             'total_price': total_price,
#         })

#         request.session['cart'] = cart  # Save cart to session
#         request.session.modified = True  # Mark session as modified

#     messages.success(request, "Item added to cart successfully.")
#     return redirect(request.META.get('HTTP_REFERER', '/'))
def add_to_cart(request, product_type, product_id):
    quantity = int(request.POST.get('quantity', 1))
    price = float(request.POST.get('price'))
    total_price = quantity * price

    if request.user.is_authenticated:
        CartItem.objects.create(
            user=request.user,
            product_type=product_type,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
        )
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        if not request.session.session_key:
            request.session.create()

        cart = request.session.get('cart', [])
        cart.append({
            'id': str(uuid.uuid4()),
            'product_type': product_type,
            'product_id': product_id,
            'quantity': quantity,
            'total_price': total_price,
        })

        request.session['cart'] = cart
        request.session.modified = True
        cart_count = len(cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': cart_count})

    messages.success(request, "Item added to cart successfully.")
    return redirect(request.META.get('HTTP_REFERER', '/'))



# cart.html view
def cart_page(request):
    if request.user.is_authenticated:
        cart_items = list(CartItem.objects.filter(user=request.user))
    else:
        cart_items = request.session.get('cart', [])

    updated_cart = []  # Store processed items

    # Assign unique keys, fetch images, and calculate unit price
    for index, item in enumerate(cart_items):
        if isinstance(item, CartItem):
            item.cart_item_key = str(item.id)  # Use database ID for authenticated users
            item.unit_price = item.total_price / item.quantity if item.quantity > 0 else 0
            product_type = item.product_type
            product_id = item.product_id
        else:
            item['cart_item_key'] = f"{item['product_id']}_{index}"  # Unique session key
            item['unit_price'] = item['total_price'] / item['quantity'] if item['quantity'] > 0 else 0
            product_type = item['product_type']
            product_id = item['product_id']

        # Fetch product images safely
        model_class = apps.get_model(app_label='netsapp', model_name=product_type.capitalize())
        try:
            product = model_class.objects.get(id=product_id)
            image_url = product.image.url if product.image else None
        except model_class.DoesNotExist:
            image_url = None

        if isinstance(item, CartItem):
            item.image_url = image_url
            updated_cart.append(item)
        else:
            item['image_url'] = image_url
            updated_cart.append(item)

    if not request.user.is_authenticated:
        request.session['cart'] = updated_cart
        request.session.modified = True

    if request.method == 'POST':
        # ✅ Handling Update Cart
        if 'update_cart' in request.POST:
            for key, value in request.POST.items():
                if key.startswith('quantity_'):
                    cart_item_key = key.replace("quantity_", "")
                    new_quantity = int(value)

                    if new_quantity < 1:
                        messages.error(request, "Quantity must be at least 1.")
                        return redirect('cart_page')

                    if request.user.is_authenticated:
                        cart_item = CartItem.objects.filter(user=request.user, id=cart_item_key).first()
                        if cart_item:
                            unit_price = cart_item.total_price / cart_item.quantity
                            cart_item.quantity = new_quantity
                            cart_item.total_price = unit_price * new_quantity
                            cart_item.save()
                    else:
                        # Update guest cart correctly
                        for item in cart_items:
                            if item['cart_item_key'] == cart_item_key:
                                unit_price = item['total_price'] / item['quantity']
                                item['quantity'] = new_quantity
                                item['total_price'] = unit_price * new_quantity
                                break
                        request.session['cart'] = cart_items  # Save updated cart
                        request.session.modified = True

            messages.success(request, "Cart updated successfully!")

        # ✅ Handling Delete Cart Item
        elif 'delete_cart_item' in request.POST:
            cart_item_key = request.POST.get('delete_cart_item')

            if not cart_item_key:
                messages.error(request, "Invalid item key.")
                return redirect('cart_page')

            if request.user.is_authenticated:
                CartItem.objects.filter(user=request.user, id=cart_item_key).delete()
            else:
                cart_items = [item for item in cart_items if item['cart_item_key'] != cart_item_key]
                request.session['cart'] = cart_items
                request.session.modified = True

            messages.success(request, "Item removed from cart!")

        return redirect('cart_page')

    cart_total = sum(item.total_price for item in cart_items) if request.user.is_authenticated else sum(item['total_price'] for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})



# delete cart
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


# fetching cart count
def cart_count_api(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart = request.session.get('cart', [])
        cart_count = len(cart)
    
    return JsonResponse({'cart_count': cart_count})


# User Registration
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create user but make it inactive until email is confirmed
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # Make user inactive until email verification
        )
        user.save()
        
    

        # Send confirmation email
        current_site = get_current_site(request)
        subject = 'Confirm your email'
        message = render_to_string('email_confirmation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject, message, 'kanalebrenda@gmail.com', [email], fail_silently=False)

        messages.success(request, "A confirmation email has been sent. Please verify your email before logging in.")
        return redirect('login')

    return render(request, 'register.html')



# User Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Please confirm your email before logging in.")
                return redirect('login')

            login(request, user)

            # Send Welcome Email
            subject = "Welcome to Matrika!"
            message = f"Hello {user.username},\n\nWelcome to Matrika! We're excited to have you on board."
            send_mail(subject, message, 'kanalebrenda@gmail.com', [user.email], fail_silently=False)

            messages.success(request, "Login successful.")

            # Check if user was trying to check out
            next_url = request.GET.get('next')
            has_cart_items = CartItem.objects.filter(user=user).exists()

            if 'checkout_redirect' in request.session:
                del request.session['checkout_redirect']
                return redirect('checkout')
            elif next_url:
                return redirect(next_url)
            elif has_cart_items:
                return redirect('cart_page')
            else:
                return redirect('Home')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')




# User Logout
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('Home')

#profile views
@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                updated_user = profile_form.save(commit=False)
                password = profile_form.cleaned_data.get('password')
                confirm_password = profile_form.cleaned_data.get('confirm_password')

                if password and password == confirm_password:
                    updated_user.set_password(password)
                    update_session_auth_hash(request, updated_user)
                elif password and password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('profile')

                updated_user.save()
                messages.success(request, "Your profile has been updated successfully!")

        elif 'update_shipping' in request.POST:
            shipping_form = ShippingAddressForm(request.POST, instance=user_profile.shipping_address)
            if shipping_form.is_valid():
                shipping_address = shipping_form.save()
                user_profile.shipping_address = shipping_address  # Link updated address to profile
                user_profile.save()
                messages.success(request, "Your shipping details have been updated!")

        elif 'update_billing' in request.POST:
            billing_form = BillingAddressForm(request.POST, instance=user_profile.billing_address)
            if billing_form.is_valid():
                billing_address = billing_form.save()
                user_profile.billing_address = billing_address  # Link updated address to profile
                user_profile.save()
                messages.success(request, "Your billing details have been updated!")

        request.session.modified = True
        return redirect('profile')

    else:
        profile_form = UserProfileForm(instance=request.user)
        shipping_form = ShippingAddressForm(instance=user_profile.shipping_address)
        billing_form = BillingAddressForm(instance=user_profile.billing_address)

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'shipping_form': shipping_form,
        'billing_form': billing_form,
        'orders': orders
    })

    
# order-detail 
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {
        'order': order
    })


#checkout
@login_required
def checkout(request):
    # Get authenticated user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

    # Check if user has a guest cart stored in session
    guest_cart = request.session.get('cart', [])

    # If guest cart exists, transfer items to authenticated user's cart
    if guest_cart:
        for item in guest_cart:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product_type=item['product_type'],
                product_id=item['product_id'],
                defaults={'quantity': item['quantity'], 'total_price': item['total_price']}
            )
            if not created:
                cart_item.quantity += item['quantity']
                # cart_item.total_price += item['total_price']
                total_price = sum(Decimal(item.total_price) for item in cart_items)
                cart_item.save()

        # Clear guest cart from session
        request.session.pop('cart', None)

        # Refresh cart items after transferring guest cart
        cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_page')

    # Get user profile and addresses
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not user_profile.shipping_address:
        user_profile.shipping_address = ShippingAddress.objects.create(user=request.user)
        user_profile.save()

    if not user_profile.billing_address:
        user_profile.billing_address = BillingAddress.objects.create(user=request.user)
        user_profile.save()

    shipping_address = user_profile.shipping_address
    billing_address = user_profile.billing_address

    # Attach product images to cart items dynamically
    for item in cart_items:
        model_class = apps.get_model(app_label='netsapp', model_name=item.product_type.capitalize())
        try:
            product = model_class.objects.get(id=item.product_id)
            item.image_url = product.image.url if hasattr(product, 'image') else None
        except model_class.DoesNotExist:
            item.image_url = None  # Default if product doesn't exist

        item.unit_price = item.total_price / item.quantity  # Calculate unit price

    # Initialize forms before conditions
    shipping_form = ShippingAddressForm(instance=shipping_address)
    billing_form = BillingAddressForm(instance=billing_address)

    if request.method == 'POST':
        if 'update_shipping' in request.POST:
            shipping_form = ShippingAddressForm(request.POST, instance=shipping_address)
            if shipping_form.is_valid():
                shipping_form.save()
                messages.success(request, "Shipping address updated successfully!")
                return redirect('checkout')

        elif 'update_billing' in request.POST:
            billing_form = BillingAddressForm(request.POST, instance=billing_address)
            if billing_form.is_valid():
                billing_form.save()
                messages.success(request, "Billing address updated successfully!")
                return redirect('checkout')

        elif 'place_order' in request.POST:
            total_price = sum(item.total_price for item in cart_items)
            shipping_fee = 0  # Free shipping
            grand_total = total_price + shipping_fee

            # Create Order
            order = Order.objects.create(
                user=request.user,
                total_price=grand_total,
                shipping_address=f"{shipping_address.street_address}, {shipping_address.town_city}, {shipping_address.country}, {shipping_address.phone}, {shipping_address.email}",
                billing_address=f"{billing_address.street_address}, {billing_address.town_city}, {billing_address.country}, {billing_address.phone}, {billing_address.email}",
            )

            order_items = []
            for item in cart_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product_name=f"{item.product_type} - {item.product_id}",
                    quantity=item.quantity,
                    price=item.unit_price,
                    total_price=item.total_price
                )
                order_items.append(order_item)

            cart_items.delete()  # Clear cart after order placement

            # Prepare email context
            email_context = {
                'user': request.user,
                'order': order,
                'order_items': order_items,
                'shipping_address': shipping_address,
                'billing_address': billing_address,
            }

            # Send email to user
            user_email_subject = f"Order Confirmation - {order.id}"
            user_email_html_message = render_to_string('emails/order_confirmation.html', email_context)
            user_email_plain_message = strip_tags(user_email_html_message)
            
            send_mail(
                user_email_subject,
                user_email_plain_message,
                'kanalebrenda@gmail.com',
                [request.user.email],
                html_message=user_email_html_message,
                fail_silently=False,
            )

            # Send email to owner
            owner_email_subject = f"New Order Received - {order.id}"
            owner_email_html_message = render_to_string('emails/order_notification.html', email_context)
            owner_email_plain_message = strip_tags(owner_email_html_message)
            
            send_mail(
                owner_email_subject,
                owner_email_plain_message,
                'kanalebrenda@gmail.com',
                ['kanalebrenda@gmail.com'],
                html_message=owner_email_html_message,
                fail_silently=False,
            )

            messages.success(request, "Your order has been placed successfully!")
            request.session['latest_order_id'] = order.id
            return redirect('order_success')

    # Calculate cart total and subtotal
    subtotal = sum(item.total_price for item in cart_items)
    shipping_fee = 0  # Free shipping
    total_price = subtotal + shipping_fee

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total_price': total_price,
        'shipping_form': shipping_form,
        'billing_form': billing_form
    })



# order_success
@login_required
def order_success(request):
    # Fetch all orders for the authenticated user and prefetch order items
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('order_items')

    if not orders.exists():
        messages.warning(request, "No orders found.")
        return render(request, 'order_success.html', {'orders': []})

    latest_order = orders.first()

    # Attach image URL to each order item by parsing product type and id from product_name
    for order in orders:
        for item in order.order_items.all():
            try:
                # Assume product_name format is "ProductType - product_id"
                parts = item.product_name.split(' - ')
                product_type = parts[0].strip()
                product_id = parts[1].strip()
                model_class = apps.get_model(app_label='netsapp', model_name=product_type.capitalize())
                product = model_class.objects.get(id=product_id)
                item.image_url = product.image.url if hasattr(product, 'image') and product.image else None
            except Exception as e:
                item.image_url = None

    return render(request, 'order_success.html', {
        'orders': orders,
        'latest_order': latest_order,
    })
    
    
# search query
def search_products(request):
    query = request.GET.get('q', '').strip().lower()  # Normalize input
    results = []

    if query:
        number_match = re.search(r'\d+', query)  # Extract numbers (e.g., "6 inch")
        numeric_value = int(number_match.group()) if number_match else None

        # Dictionary to handle category recognition & plural support
        category_map = {
            "mattress": ["mattress", "mattresses"],
            "pillow": ["pillow", "pillows"],
            "bedsheet": ["bedsheet", "bedsheets"],
            "duvet": ["duvet", "duvets"],
        }

        # Fix for "plain mattress" and "quilted mattress"
        mattress_type_map = {
            "plain mattress": "plain",
            "plain mattresses": "plain",
            "quilted mattress": "quilted",
            "quilted mattresses": "quilted",
        }

        mattresses = Mattress.objects.none()
        pillows = Pillow.objects.none()
        bedsheets = Bedsheet.objects.none()
        duvets = Duvet.objects.none()

        # Check for exact mattress type searches
        if query in mattress_type_map:
            mattresses = Mattress.objects.filter(type=mattress_type_map[query])
        elif query in category_map["mattress"]:
            mattresses = Mattress.objects.all()
        else:
            mattresses = Mattress.objects.filter(
                Q(type__istartswith=query) |  
                Q(size__istartswith=query) |  
                (Q(thickness=numeric_value) if numeric_value else Q())  
            )

        if query in category_map["pillow"]:
            pillows = Pillow.objects.all()
        else:
            pillows = Pillow.objects.filter(
                Q(material__istartswith=query)
            )

        if query in category_map["bedsheet"]:
            bedsheets = Bedsheet.objects.all()
        else:
            bedsheets = Bedsheet.objects.filter(
                Q(size__istartswith=query) |
                Q(material__istartswith=query) |
                Q(color__istartswith=query)
            )

        if query in category_map["duvet"]:
            duvets = Duvet.objects.all()
        else:
            duvets = Duvet.objects.filter(
                Q(size__istartswith=query) |
                Q(material__istartswith=query) |
                Q(color__istartswith=query)
            )

        # Merge all results
        results = list(mattresses) + list(pillows) + list(bedsheets) + list(duvets)

    return render(request, 'search_results.html', {'results': results, 'query': query})



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email confirmed! You can now log in.")
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')