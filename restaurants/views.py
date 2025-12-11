from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import role_required
from .models import Restaurant, MenuItem
from django.utils import timezone


# ============================
# OWNER: MENU CRUD
# ============================

@role_required(['restaurant'])
def menu_list(request, resto_id):
    resto = get_object_or_404(Restaurant, id=resto_id, owner=request.user)
    menus = resto.menu_items.all()
    return render(request, 'restaurants/menu_list.html', {
        'resto': resto,
        'menus': menus
    })


@role_required(['restaurant'])
def menu_create(request, resto_id):
    resto = get_object_or_404(Restaurant, id=resto_id, owner=request.user)

    if request.method == 'POST':
        MenuItem.objects.create(
            restaurant=resto,
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            description=request.POST.get('description')
        )
        return redirect('restaurants:menu_list', resto_id=resto.id)

    return render(request, 'restaurants/menu_create.html', {
        'resto': resto
    })


@role_required(['restaurant'])
def menu_edit(request, resto_id, id):
    resto = get_object_or_404(Restaurant, id=resto_id, owner=request.user)
    menu = get_object_or_404(MenuItem, id=id, restaurant=resto)

    if request.method == 'POST':
        menu.name = request.POST.get('name')
        menu.price = request.POST.get('price')
        menu.description = request.POST.get('description')
        menu.save()

        return redirect('restaurants:menu_list', resto_id=resto.id)

    return render(request, 'restaurants/menu_edit.html', {
        'resto': resto,
        'menu': menu
    })


@role_required(['restaurant'])
def menu_delete(request, resto_id, id):
    resto = get_object_or_404(Restaurant, id=resto_id, owner=request.user)
    menu = get_object_or_404(MenuItem, id=id, restaurant=resto)
    menu.delete()

    return redirect('restaurants:menu_list', resto_id=resto.id)


# ============================
# ADMIN: RESTO CRUD
# ============================

@role_required(['admin'])
def restaurant_list(request):
    restos = Restaurant.objects.all()
    return render(request, 'restaurants/list.html', {'restos': restos})


@role_required(['admin'])
def restaurant_create(request):
    if request.method == 'POST':
        Restaurant.objects.create(
            owner_id=request.POST.get('owner'),
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            description=request.POST.get('description')
        )
        return redirect('restaurants:list')

    return render(request, 'restaurants/create.html')


@role_required(['admin'])
def restaurant_edit(request, id):
    resto = get_object_or_404(Restaurant, id=id)

    if request.method == 'POST':
        resto.name = request.POST.get('name')
        resto.address = request.POST.get('address')
        resto.description = request.POST.get('description')
        resto.save()

        return redirect('restaurants:list')

    return render(request, 'restaurants/edit.html', {'resto': resto})


@role_required(['admin'])
def restaurant_delete(request, id):
    resto = get_object_or_404(Restaurant, id=id)
    resto.delete()

    return redirect('restaurants:list')



@role_required(['restaurant'])  # Perbaiki: tambahkan allowed_roles
def dashboard(request):
    # HAPUS baris ini: from accounts.decorators import role_required
    # HAPUS baris ini: decorated_view = role_required(allowed_roles=['Restaurant'])(dashboard)
    
    # Logika untuk mengambil data dashboard (misalnya pesanan, menu, dll.)
    # Contoh: ambil resto milik user
    try:
        resto = Restaurant.objects.get(owner=request.user)
    except Restaurant.DoesNotExist:
       return redirect('restaurants:create')
    
    context = {
        'greeting': 'Selamat datang di Dashboard Restoran Anda!',
        'resto': resto,  # Tambahkan data relevan
        # ... data lainnya, misalnya menus = resto.menu_items.all() jika perlu
    }
    return render(request, 'dashboard/restaurant_dashboard.html', context)  # Perbaiki path template jika perlu



# ============================
# ORDER MANAGEMENT RESTAURANT
# ============================

def restaurant_orders(request):
    orders = Order.objects.filter(restaurant=request.user).order_by("-created_at")
    return render(request, "restaurant/orders.html", {"orders": orders})

def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, restaurant=request.user)
    order.status = "accepted"
    order.save()
    return redirect("restaurants:restaurant_orders")

def prepare_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, restaurant=request.user)
    order.status = "preparing"
    order.save()
    return redirect("restaurants:restaurant_orders")

def ready_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, restaurant=request.user)
    order.status = "ready_for_pickup"
    order.save()
    return redirect("restaurants:restaurant_orders")

def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        method = request.POST["method"]
        amount = order.total_price

        Payment.objects.update_or_create(
            order=order,
            defaults={
                "method": method,
                "status": "paid",
                "amount": amount,
                "paid_at": timezone.now()
            }
        )

        order.payment_status = "paid"
        order.save()

        messages.success(request, "Payment confirmed!")
        return redirect("restaurants:restaurant_orders")

    return render(request, "restaurant/payment.html", {"order": order})