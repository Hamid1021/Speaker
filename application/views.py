from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from application.Entities.order_model import Order, OrderSpeaker
from extensions.utils import gregorian_converter_date, send_message_by_template, jalali_converter_date
from django.utils import timezone
from django.db.models import Count
from application.Entities.Speaker_model import Speaker


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
    return HttpResponse("Access Denied", status=403)


def faill_action(request):
    if 'redirected' in request.session:
        del request.session['redirected']
        return render(request, "success_action.html")
    context = {
        
    }
    return render(request, "faill_action.html", context)




def assign_orders_to_speakers():
    orders = Order.objects.filter(is_assign=False).order_by('date', 'time')
    eligible_speakers = Speaker.objects.annotate(num_lectures=Count('orderspeaker__order')).filter(
        status=True,
        is_deleted=False
    ).order_by('total_number_of_lectures', 'register_time', 'name', 'family')
    for order in orders:
        for speaker in eligible_speakers:
            if speaker.today_number_of_lectures < 2:
                # شمارنده روضه های کل
                speaker.total_number_of_lectures += 1
                # شمارنده روضه های امروز
                speaker.today_number_of_lectures += 1
                speaker.save()
                order.is_assign = True
                order.save()
                OrderSpeaker.objects.create(order=order, speaker=speaker)
                break

def reset_today(request):
    eligible_speakers = Speaker.objects.annotate(num_lectures=Count('orderspeaker__order')).filter(
        status=True,
        is_deleted=False)
    for s in eligible_speakers:
        s.today_number_of_lectures = 0
        s.save()
    return redirect(reverse("application:assign"))


def do_assign(request):
    assign_orders_to_speakers()
    return redirect(reverse("application:assign"))


def assign(request):
    today = timezone.localtime(timezone.now())
    today = today.date()
    all_order = OrderSpeaker.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
    request.session['redirected'] = True
    context = {
        "object_list":all_order
    }
    return render(request, "assign.html", context)


def sent_to_channel(request):
    if 'redirected' in request.session:
        del request.session['redirected']   
        try:
            today = timezone.localtime(timezone.now())
            today = today.date()
            today_order_speaker = OrderSpeaker.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
            for i in today_order_speaker:
                send_message_by_template(
                    phone=i.order.phone, date=jalali_converter_date(i.order.date), time=str(i.order.time)[:5], num_attendees=i.order.num_attendees,
                    gender_attendees=i.order.gender_attendees,
                    education_min_attendees=i.order.education_min_attendees, education_max_attendees=i.order.education_max_attendees,
                    city=i.order.city, topic=i.order.topic, obj=i, speaker=i.speaker.get_fullname(), chatID="10237460", 
                )
            return render(request, "success_send_message.html")
        except Exception as err:
            print(err)
            return render(request, "failled_send_message.html")
    return HttpResponse("شما دسترسی ندارید", status=403)
