from django.db.models import Sum

from accounting.constants import Category

BACKGROUND_COLOR = [
    "#fd7c7c",
    "#fdfd7c",
    "#7cfd7c",
    "#f6fd7c",
    "#7cfd83",
    "#7cf6fd",
    "#80fd7c",
    "#7cfdf9",
    "#7c80fd",
    "#7cfafd",
    "#7f7cfd",
    "#fd7cfa",
    "#7c7dfd",
    "#fc7cfd",
    "#fd7c7d",
    "#ee7cfd",
    "#fd7c8b",
    "#fdee7c",
]

HOVER_BACKGROUND_COLOR = [
    "#fdbd7c",
    "#bdfd7c",
    "#7cfdbd",
    "#b6fd7c",
    "#7cfdc3",
    "#7cb6fd",
    "#7cfdb9",
    "#7cc1fd",
    "#b97cfd",
    "#7cbafd",
    "#c07cfd",
    "#fd7cba",
    "#bb7cfd",
    "#fd7cbe",
    "#fdbb7c",
    "#fd7ccc",
    "#fdae7c",
    "#ccfd7c",
]


def get_pie_data(context: dict):

    total_amount_per_category = {cat.value: 0 for cat in Category}

    for trip in context["trips"]:
        sum_by_category = trip.expense_set.values("category").annotate(
            sum=Sum("amount")
        )
        for category in sum_by_category:
            total_amount_per_category[category["category"]] += float(category["sum"])

    context["labels"] = list(total_amount_per_category.keys())
    context["data"] = list(total_amount_per_category.values())
    context["background_color"] = BACKGROUND_COLOR[: len(context["labels"])]
    context["hover_background_color"] = HOVER_BACKGROUND_COLOR[: len(context["labels"])]
    return context
