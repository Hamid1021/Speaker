from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from application.Entities.order_model import Order, SelectOrderSpeaker, AssignOrderSpeaker
from extensions.utils import gregorian_converter_date, send_message_by_template, jalali_converter_date
from django.utils import timezone
from application.Entities.Speaker_model import Speaker
from application.forms import SelectOrderSpeakerForm, OrderSpeakerForm
from datetime import timedelta, datetime
from django.db.models import Count, Sum, Min
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
import jdatetime
import pytz
import json


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
            # بررسی اینکه سخنران درخواست داده است یا خیر
            has_requested = SelectOrderSpeaker.objects.filter(speaker=speaker, order=order).exists()
            
            is_pass_a_half = AssignOrderSpeaker.objects.filter(
                    speaker=speaker,
                    date__year=today.year, date__month=today.month, date__day=today.day
                ).first()
            if has_requested:
                # بررسی تعداد سفارش‌های امروز سخنران
                today_orders_count = AssignOrderSpeaker.objects.filter(
                    speaker=speaker,
                    date__year=today.year, date__month=today.month, date__day=today.day
                ).count()

                # اگر تعداد سفارش‌های امروز کمتر از 2 باشد، اختصاص سفارش به سخنران
                if today_orders_count < 2:
                    if is_pass_a_half:
                        prev_order_time = datetime.combine(today, is_pass_a_half.order.time)
                        current_order_time = datetime.combine(today, order.time)
                        if current_order_time - prev_order_time >= timedelta(minutes=30):
                            order.is_assign = True
                            order.save()
                            AssignOrderSpeaker.objects.create(order=order, speaker=speaker)
                            break
                    else:
                        order.is_assign = True
                        order.save()
                        AssignOrderSpeaker.objects.create(order=order, speaker=speaker)
                        break


def do_assign(request):
    assign_orders_to_speakers()
    return redirect(reverse("application:assign"))


def assign(request):
    all_order = AssignOrderSpeaker.objects.filter(is_message_send=False)
    start_time = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')
    # start_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['redirected'] = True
    context = {
        "object_list": all_order,
        "start_time": start_time.replace(" ", "T")
    }
    return render(request, "assign.html", context)


def change_status(request, speaker_id, order_id):
    get_speaker = Speaker.objects.filter(user=request.user, id=speaker_id).first()
    if not get_speaker:
        return redirect('application:select_order_by_speaker')

    order = Order.objects.get(id=order_id)

    if order.status == "uc":
        order.status = "c"
    else:
        order.status = "uc"
    order.save()

    return redirect(reverse("application:speaker_assigned_orders", args=[speaker_id]))


def speaker_assigned_orders(request, speaker_id):
    speaker = Speaker.objects.filter(user=request.user, id=speaker_id).first()
    if not speaker:
        return redirect('application:select_order_by_speaker')
    
    assigned_orders = AssignOrderSpeaker.objects.filter(speaker=speaker)
    
    context = {
        'speaker': speaker,
        'assigned_orders': assigned_orders
    }
    return render(request, 'speaker_assigned_orders.html', context)


def edit_assign(request, pk):
    order = get_object_or_404(AssignOrderSpeaker, id=pk)
    if request.method == 'POST':
        form = OrderSpeakerForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('application:assign')
    else:
        form = OrderSpeakerForm(instance=order)
    return render(request, 'edit_assign.html', {'form': form})


def list_assign(request):
    all_order = AssignOrderSpeaker.objects.filter(is_message_send=True)
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
            order_speaker = AssignOrderSpeaker.objects.filter(is_message_send=False)
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


def success_select_order(request):
    if 'redirected' in request.session:
        del request.session['redirected']
        return render(request, "success_select_order.html")
    return redirect('application:list_assign')


def select_order_by_speaker(request):
    context = {}
    speaker = instance = None
    if request.user.is_authenticated:
        speaker = Speaker.objects.filter(user=request.user).first()
        instance = SelectOrderSpeaker.objects.filter(speaker=speaker).first()
        all_orders = Order.objects.get_all_not_assign()
        if instance:
            selected_orders = instance.order.exclude(is_assign=True)
            all_orders = all_orders.exclude(id__in=selected_orders.values_list('id', flat=True))
        else:
            selected_orders = []
        
        if request.method == 'POST':
            form = SelectOrderSpeakerForm(request.POST, user=request.user, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.speaker = speaker
                obj.save()
                form.save_m2m()
                request.session['redirected'] = True
                return redirect("application:success_select_order")
        else:
            form = SelectOrderSpeakerForm(user=request.user, instance=instance)

        context["form"] = form
        context["all_orders"] = all_orders
        context["selected_orders"] = selected_orders
    
    return render(request, 'select_order_by_speaker.html', context)




def get_jalali_weeks():
    first_order_date = AssignOrderSpeaker.objects.aggregate(first_date=Min('date'))['first_date']
    if not first_order_date:
        return []

    start_date = jdatetime.date.fromgregorian(date=first_order_date.date())
    today = jdatetime.date.today()
    weeks = []
    while start_date <= today:
        weeks.append(start_date)
        start_date += jdatetime.timedelta(days=7)
    return weeks

def get_jalali_weekday_counts(start_of_week):
    end_of_week = start_of_week + jdatetime.timedelta(days=6)
    start_of_week_gregorian = datetime.combine(start_of_week, datetime.min.time()).replace(tzinfo=pytz.UTC)
    end_of_week_gregorian = datetime.combine(end_of_week, datetime.min.time()).replace(tzinfo=pytz.UTC)

    assigned_orders = AssignOrderSpeaker.objects.filter(date__range=[start_of_week_gregorian, end_of_week_gregorian])

    weekdays = {
        "شنبه": 0,
        "یکشنبه": 1,
        "دوشنبه": 2,
        "سه‌شنبه": 3,
        "چهارشنبه": 4,
        "پنجشنبه": 5,
        "جمعه": 6,
    }

    weekday_counts = {day: 0 for day in weekdays.keys()}
    
    for assigned_order in assigned_orders:
        jalali_date = jdatetime.date.fromgregorian(date=assigned_order.date)
        weekday_name = jalali_date.strftime('%A')
        weekday_name_fa = {
            'Saturday': 'شنبه',
            'Sunday': 'یکشنبه',
            'Monday': 'دوشنبه',
            'Tuesday': 'سه‌شنبه',
            'Wednesday': 'چهارشنبه',
            'Thursday': 'پنجشنبه',
            'Friday': 'جمعه'
        }.get(weekday_name, '')
        
        if weekday_name_fa in weekday_counts:
            weekday_counts[weekday_name_fa] += 1

    return weekday_counts

def reports(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    
    week_param = request.GET.get('week')
    weeks = get_jalali_weeks()
    if week_param:
        try:
            start_of_week = datetime.strptime(week_param, '%Y-%m-%d').date()
        except ValueError:
            start_of_week = datetime.today().date() - timedelta(days=datetime.today().weekday())
        selected_week = week_param
    else:
        if weeks:
            start_of_week = weeks[-1].togregorian()  # آخرین مورد لیست weeks را به میلادی تبدیل کنید
            selected_week = start_of_week.strftime('%Y-%m-%d')
        else:
            today = datetime.today().date()
            start_of_week = today - timedelta(days=today.weekday())
            selected_week = start_of_week.strftime('%Y-%m-%d')

    # تعداد کل افراد شرکت کننده
    total_attendees = Order.objects.aggregate(total_attendees=Sum('num_attendees'))

    # تعداد کل روضه‌های انجام شده در امروز
    today = datetime.today()
    total_today = AssignOrderSpeaker.objects.filter(date__date=today.date()).count()

    # تعداد کل روضه‌های انجام شده در این ماه
    total_month = AssignOrderSpeaker.objects.filter(date__year=today.year, date__month=today.month).count()

    # تعداد کل روضه‌های انجام شده در این سال
    total_year = AssignOrderSpeaker.objects.filter(date__year=today.year).count()

    # لیست همه شهرها و تعداد سفارشات هر شهر
    city_stats = Order.objects.values('city').annotate(count=Count('id')).order_by('-count')

    # لیست حداقل و حداکثر مدارک تحصیلی و تعداد سفارشات هر کدام
    education_min_stats = Order.objects.values('education_min_attendees').annotate(count=Count('id')).order_by('-count')
    education_max_stats = Order.objects.values('education_max_attendees').annotate(count=Count('id')).order_by('-count')

    # جنسیت افراد شرکت کننده و تعداد سفارشات
    gender_stats = Order.objects.values('gender_attendees').annotate(count=Count('id')).order_by('-count')

    # تعداد سفارشات در روزهای هفته انتخابی
    weekday_counts = get_jalali_weekday_counts(start_of_week)
    
    context = {
        'total_attendees': total_attendees['total_attendees'],
        'total_today': total_today,
        'total_month': total_month,
        'total_year': total_year,
        'city_stats': city_stats,
        'education_min_stats': education_min_stats,
        'education_max_stats': education_max_stats,
        'gender_stats': gender_stats,
        'weekday_counts': weekday_counts,
        'weeks': weeks,
        'selected_week': selected_week,
    }
    return render(request, 'reports.html', context)


def reports1(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    week_param = request.GET.get('week')
    weeks = get_jalali_weeks()
    if week_param:
        try:
            start_of_week = datetime.strptime(week_param, '%Y-%m-%d').date()
        except ValueError:
            start_of_week = datetime.today().date() - timedelta(days=datetime.today().weekday())
        selected_week = week_param
    else:
        if weeks:
            start_of_week = weeks[-1].togregorian()  # آخرین مورد لیست weeks را به میلادی تبدیل کنید
            selected_week = start_of_week.strftime('%Y-%m-%d')
        else:
            today = datetime.today().date()
            start_of_week = today - timedelta(days=today.weekday())
            selected_week = start_of_week.strftime('%Y-%m-%d')

    # تعداد کل افراد شرکت کننده
    total_attendees = Order.objects.aggregate(total_attendees=Sum('num_attendees'))

    # تعداد کل روضه‌های انجام شده در امروز
    today = datetime.today()
    total_today = AssignOrderSpeaker.objects.filter(date__date=today.date()).count()

    # تعداد کل روضه‌های انجام شده در این ماه
    total_month = AssignOrderSpeaker.objects.filter(date__year=today.year, date__month=today.month).count()

    # تعداد کل روضه‌های انجام شده در این سال
    total_year = AssignOrderSpeaker.objects.filter(date__year=today.year).count()

    # لیست همه شهرها و تعداد سفارشات هر شهر
    city_stats = list(Order.objects.values('city').annotate(count=Count('id')).order_by('-count'))

    # لیست حداقل و حداکثر مدارک تحصیلی و تعداد سفارشات هر کدام
    education_min_stats = list(Order.objects.values('education_min_attendees').annotate(count=Count('id')).order_by('-count'))
    education_max_stats = list(Order.objects.values('education_max_attendees').annotate(count=Count('id')).order_by('-count'))

    # جنسیت افراد شرکت کننده و تعداد سفارشات
    gender_stats = list(Order.objects.values('gender_attendees').annotate(count=Count('id')).order_by('-count'))

    # تعداد سفارشات در روزهای هفته انتخابی
    weekday_counts = get_jalali_weekday_counts(start_of_week)

    context = {
        'total_attendees': total_attendees['total_attendees'],
        'total_today': total_today,
        'total_month': total_month,
        'total_year': total_year,
        'city_stats': json.dumps(city_stats),
        'education_min_stats': json.dumps(education_min_stats),
        'education_max_stats': json.dumps(education_max_stats),
        'gender_stats': json.dumps(gender_stats),
        'weekday_counts': json.dumps(weekday_counts),
        'weeks': weeks,
        'selected_week': selected_week,
    }
    return render(request, 'reports1.html', context)
