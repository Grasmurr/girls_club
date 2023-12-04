from django.http import JsonResponse
from .models import Event, MemberGirl, Newsletter, UnregisteredGirl
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json


@csrf_exempt
@require_http_methods(["POST"])
def create_event(request):
    data = json.loads(request.body)
    event = Event.objects.create(**data)
    return JsonResponse({'id': event.id, 'name': event.name})


@csrf_exempt
@require_http_methods(["POST"])
def update_event(request, name):
    data = json.loads(request.body)
    try:
        event = Event.objects.get(name=name)
        for field, value in data.items():
            setattr(event, field, value) if value is not None else None
        event.save()
        return JsonResponse({"status": "updated"})
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)



@csrf_exempt
@require_http_methods(["DELETE"])
def delete_event(request, name):
    Event.objects.filter(name=name).delete()
    return JsonResponse({"status": "deleted"})


@csrf_exempt
@require_http_methods(["GET"])
def get_event(request, name):
    try:
        event = Event.objects.get(name=name)
        return JsonResponse(model_to_dict(event))
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_event(request):
    try:
        event = Event.objects.all().values()
        return JsonResponse({'data': list(event)}, safe=False)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def create_member_girl(request):
    data = json.loads(request.body)
    member_girl = MemberGirl.objects.create(**data)
    return JsonResponse({'unique_id': member_girl.telegram_id, 'full_name': member_girl.full_name})


@csrf_exempt
@require_http_methods(["POST"])
def update_member_girl(request, telegram_id):
    data = json.loads(request.body)
    try:
        member_girl = MemberGirl.objects.get(telegram_id=telegram_id)
        for field, value in data.items():
            setattr(member_girl, field, value) if value is not None else None
        member_girl.save()
        return JsonResponse({"status": "updated"})
    except MemberGirl.DoesNotExist:
        return JsonResponse({"error": "MemberGirl not found"}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_member_girl(request, telegram_id):
    MemberGirl.objects.filter(telegram_id=telegram_id).delete()
    return JsonResponse({"status": "deleted"})


@csrf_exempt
@require_http_methods(["GET"])
def get_member_girl(request, telegram_id):
    try:
        member_girl = MemberGirl.objects.get(telegram_id=telegram_id)
        return JsonResponse(model_to_dict(member_girl))
    except MemberGirl.DoesNotExist:
        return JsonResponse({'error': 'MemberGirl not found'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_all(request):
    try:
        member_girl = MemberGirl.objects.all().values()
        return JsonResponse({'data': list(member_girl)}, safe=False)
    except MemberGirl.DoesNotExist:
        return JsonResponse({'error': 'MemberGirl not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def create_or_update_newsletter(request, number=None):
    data = json.loads(request.body)

    newsletter, created = Newsletter.objects.update_or_create(
        number=number,
        defaults=data
    )
    status = "created" if created else "updated"
    return JsonResponse({"status": status, "number": newsletter.number})


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_newsletter(request, number):
    Newsletter.objects.filter(number=number).delete()
    return JsonResponse({"status": "deleted"})


@csrf_exempt
@require_http_methods(["GET"])
def get_newsletter(request, number):
    try:
        newsletter = Newsletter.objects.get(number=number)
        return JsonResponse(model_to_dict(newsletter))
    except Newsletter.DoesNotExist:
        return JsonResponse({'error': 'Newsletter not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def create_unregistered_girl(request):
    data = json.loads(request.body)
    member_girl = UnregisteredGirl.objects.create(**data)
    return JsonResponse({'unique_id': member_girl.telegram_id})


@csrf_exempt
@require_http_methods(["POST"])
def update_unregistered_girl(request, telegram_id):
    data = json.loads(request.body)
    try:
        member_girl = UnregisteredGirl.objects.get(telegram_id=telegram_id)
        for field, value in data.items():
            setattr(member_girl, field, value) if value is not None else None
        member_girl.save()
        return JsonResponse({"status": "updated"})
    except UnregisteredGirl.DoesNotExist:
        return JsonResponse({"error": "UnregisteredGirl not found"}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_unregistered_girl(request, telegram_id):
    try:
        member_girl = UnregisteredGirl.objects.get(telegram_id=telegram_id)
        return JsonResponse(model_to_dict(member_girl))
    except UnregisteredGirl.DoesNotExist:
        return JsonResponse({'error': 'MemberGirl not found'}, status=404)
