from django.shortcuts import render

from engine.views import not_implemented


def candidate_list(request):
    return render(request, "candidates/list.html")


def candidate_create(request):
    return not_implemented(request, feature="Создание кандидата")


def candidate_detail(request, candidate_id):
    return not_implemented(request, feature="Карточка кандидата")


def candidate_update(request, candidate_id):
    return not_implemented(request, feature="Редактирование кандидата")


def resume_list(request, candidate_id):
    return not_implemented(request, feature="Список резюме")


def resume_create(request, candidate_id):
    return not_implemented(request, feature="Создание резюме")


def resume_detail(request, candidate_id, resume_id):
    return not_implemented(request, feature="Просмотр резюме")


def resume_update(request, candidate_id, resume_id):
    return not_implemented(request, feature="Редактирование резюме")


def public_resume(request, public_id):
    return not_implemented(request, feature="Публичное резюме")
