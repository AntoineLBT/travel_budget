from enum import Enum


class Category(Enum):
    TRANSPORT = "transport"
    GROCERY = "grocery"
    ACTIVITY = "activity"
    RESTAURANT = "restaurant"
    MEDICAL = "medical"
    ADMINISTRATIVE = "administrative"
    ACCOMMODATION = "accommodation"


CATEGORY_CHOICES = [
    (Category.TRANSPORT.value, "Transport"),
    (Category.GROCERY.value, "Grocery"),
    (Category.ACTIVITY.value, "Activity"),
    (Category.RESTAURANT.value, "Restaurant"),
    (Category.ADMINISTRATIVE.value, "Administrative"),
    (Category.ACCOMMODATION.value, "Accommodation"),
]

CURRENCY_CHOICES = [
    ("AUD", "Australian Dollar"),
    ("BGN", "Bulgarian Lev"),
    ("BRL", "Brazilian Real"),
    ("CAD", "Canadian Dollar"),
    ("CHF", "Swiss Franc"),
    ("CNY", "Chinese Yuan"),
    ("CZK", "Czech Koruna"),
    ("DKK", "Danish Krone"),
    ("EUR", "Euro"),
    ("GBP", "British Pound Sterling"),
    ("HKD", "Hong Kong Dollar"),
    ("HUF", "Hungarian Forint"),
    ("IDR", "Indonesian Rupiah"),
    ("ILS", "Israeli New Shekel"),
    ("INR", "Indian Rupee"),
    ("ISK", "Icelandic Króna"),
    ("JPY", "Japanese Yen"),
    ("KRW", "South Korean Won"),
    ("MXN", "Mexican Peso"),
    ("MYR", "Malaysian Ringgit"),
    ("NOK", "Norwegian Krone"),
    ("NZD", "New Zealand Dollar"),
    ("PHP", "Philippine Peso"),
    ("PLN", "Polish Złoty"),
    ("RON", "Romanian Leu"),
    ("SEK", "Swedish Krona"),
    ("SGD", "Singapore Dollar"),
    ("THB", "Thai Baht"),
    ("TRY", "Turkish Lira"),
    ("USD", "United States Dollar"),
    ("ZAR", "South African Rand"),
]
