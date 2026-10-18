from django.shortcuts import render


def home(request):
    return render(request, "main.html")


def not_implemented(request, feature="Эта функция", **kwargs):
    return render(
        request,
        "errors/501_not_implemented.html",
        {"feature": feature},
        status=501,
    )

