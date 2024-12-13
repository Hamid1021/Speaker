from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from application.Entities.order_model import Order, OrderSpeaker
from extensions.utils import gregorian_converter_date, send_message_by_template, jalali_converter_date
from django.utils import timezone
from django.db.models import Count
from application.Entities.Speaker_model import Speaker
from application.forms import OrderSpeakerForm

def index(request):
    status = None
    if request.POST:
        data = request.POST
        phone = data.get("phone")
        date = data.get("date")
        time = data.get("time")
        num_attendees = data.get("num_attendees")
        gender_attendees = data.get("gender_attendees")
        education_min_attendees = data.get("education_min_attendees")
        education_max_attendees = data.get("education_max_attendees")
        city = data.get("city")
        topic = data.get("topic")
        obj, status = Order.objects.tryCreateObject(
            phone = phone,
            date = gregorian_converter_date(data.get("date")),
            time = time,
            num_attendees = num_attendees,
            gender_attendees = gender_attendees,
            education_min_attendees = education_min_attendees,
            education_max_attendees = education_max_attendees,
            city = city,
            topic = topic,
        )
        request.session['redirected'] = True
        if status:
            send_message_by_template(
                phone=phone, date=date, time=time, num_attendees=num_attendees, gender_attendees=gender_attendees,
                education_min_attendees=education_min_attendees, education_max_attendees=education_max_attendees,
                city=city, topic=topic, obj=obj, chatID="10237508"
            )
            return redirect(reverse("application:success_action"))
        else:
            return redirect(reverse("application:faill_action"))

    context = {

    }
    return render(request, "index.html", context)


def success_action(request):
    if 'redirected' in request.session:
        del request.session['redirected']
        return render(request, "success_action.html")
    return redirect('application:assign')


def faill_action(request):
    if 'redirected' in request.session:
        del request.session['redirected']
        return render(request, "faill_action.html")
    return redirect('application:assign')


def assign_orders_to_speakers():
    today = timezone.localtime(timezone.now()).date()
    orders = Order.objects.filter(is_assign=False).order_by('date', 'time')
    eligible_speakers = Speaker.objects.filter(
        status=True,
        is_deleted=False
    ).order_by('total_number_of_lectures', 'register_time', 'name', 'family')
    for order in orders:
        for speaker in eligible_speakers:
            today_orders_count = OrderSpeaker.objects.filter(
                speaker=speaker,
                date__year=today.year, date__month=today.month, date__day=today.day
            ).count()
            print(speaker.name, today_orders_count)
            
            if today_orders_count < 2:
                order.is_assign = True
                order.save()
                OrderSpeaker.objects.create(order=order, speaker=speaker)
                break


def do_assign(request):
    assign_orders_to_speakers()
    return redirect(reverse("application:assign"))


def assign(request):
    all_order = OrderSpeaker.objects.filter(is_message_send=False)
    start_time = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
    # start_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['redirected'] = True
    context = {
        "object_list":all_order,
        "start_time":start_time.replace(" ", "T")
    }
    return render(request, "assign.html", context)


def edit_assign(request, pk):
    order = get_object_or_404(OrderSpeaker, id=pk)
    if request.method == 'POST':
        form = OrderSpeakerForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('application:assign')
    else:
        form = OrderSpeakerForm(instance=order)
    return render(request, 'edit_assign.html', {'form': form})


def list_assign(request):
    all_order = OrderSpeaker.objects.filter(is_message_send=True)
    context = {
        "object_list":all_order,
    }
    return render(request, "all_assign.html", context)


def sent_to_channel(request):
    if 'redirected' in request.session:
        del request.session['redirected']   
        try:
            today = timezone.localtime(timezone.now())
            today = today.date()
            order_speaker = OrderSpeaker.objects.filter(is_message_send=False)
            for i in order_speaker:
                # شمارنده روضه ها 
                i.speaker.total_number_of_lectures += 1
                i.speaker.save()
                send_message_by_template(
                    phone=i.order.phone, date=jalali_converter_date(i.order.date), time=str(i.order.time)[:5], num_attendees=i.order.num_attendees,
                    gender_attendees=i.order.gender_attendees,
                    education_min_attendees=i.order.education_min_attendees, education_max_attendees=i.order.education_max_attendees,
                    city=i.order.city, topic=i.order.topic, obj=i, speaker=i.speaker.get_fullname(), chatID="10237460", 
                )
            return render(request, "success_send_message.html")
        except Exception as err:
            return render(request, "failled_send_message.html")
    return redirect('application:assign')
