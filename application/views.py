from django.shortcuts import render
from application.Entities.order_model import Order
from application.send_message import send_message_to_channel

def index(request):
    status_message = ""
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

        obj, status, status_message = Order.objects.tryCreateObject(
            phone = phone,
            date = date,
            time = time,
            num_attendees = num_attendees,
            gender_attendees = gender_attendees,
            education_min_attendees = education_min_attendees,
            education_max_attendees = education_max_attendees,
            city = city,
            topic = topic,
        )

        if status:
            with open("message_template.txt", "+r", encoding='utf-8') as f:
                file = f.read()
                file = file.format(
                    phone = phone,
                    date = date,
                    time = time,
                    num_attendees = num_attendees,
                    gender_attendees = gender_attendees,
                    education_min_attendees = education_min_attendees,
                    education_max_attendees = education_max_attendees,
                    city = city,
                    topic = topic,
                    status = "انجام شد" if obj.status == "c" else "انجام نشده"
                )
            channel_message, channel_status = send_message_to_channel("sendMessage", 10237508, topic, file)
            obj.related_message = channel_message
            obj.save()

    context = {
        "status":status,
        "status_message":status_message,
    }
    return render(request, "index.html", context)
