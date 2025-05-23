# Generated by Django 4.2.11 on 2024-04-09 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Afghanistan", "AFGHANISTAN"),
                    ("Albania", "ALBANIA"),
                    ("Algeria", "ALGERIA"),
                    ("Andorra", "ANDORRA"),
                    ("Angola", "ANGOLA"),
                    ("Antigua & Deps", "ANTIGUA_AND_DEPS"),
                    ("Argentina", "ARGENTINA"),
                    ("Armenia", "ARMENIA"),
                    ("Australia", "AUSTRALIA"),
                    ("Austria", "AUSTRIA"),
                    ("Azerbaijan", "AZERBAIJAN"),
                    ("Bahamas", "BAHAMAS"),
                    ("Bahrain", "BAHRAIN"),
                    ("Bangladesh", "BANGLADESH"),
                    ("Barbados", "BARBADOS"),
                    ("Belarus", "BELARUS"),
                    ("Belgium", "BELGIUM"),
                    ("Belize", "BELIZE"),
                    ("Benin", "BENIN"),
                    ("Bhutan", "BHUTAN"),
                    ("Bolivia", "BOLIVIA"),
                    ("Bosnia Herzegovina", "BOSNIA_HERZEGOVINA"),
                    ("Botswana", "BOTSWANA"),
                    ("Brazil", "BRAZIL"),
                    ("Brunei", "BRUNEI"),
                    ("Bulgaria", "BULGARIA"),
                    ("Burkina", "BURKINA"),
                    ("Burundi", "BURUNDI"),
                    ("Cambodia", "CAMBODIA"),
                    ("Cameroon", "CAMEROON"),
                    ("Canada", "CANADA"),
                    ("Cape Verde", "CAPE_VERDE"),
                    ("Central African Rep", "CENTRAL_AFRICAN_REP"),
                    ("Chad", "CHAD"),
                    ("Chile", "CHILE"),
                    ("China", "CHINA"),
                    ("Colombia", "COLOMBIA"),
                    ("Comoros", "COMOROS"),
                    ("Congo", "CONGO"),
                    ("Congo {Democratic Rep}", "CONGO_REP_DEMO"),
                    ("Costa Rica", "COSTA_RICA"),
                    ("Croatia", "CROATIA"),
                    ("Cuba", "CUBA"),
                    ("Cyprus", "CYPRUS"),
                    ("Czech Republic", "CZECH_REPUBLIC"),
                    ("Denmark", "DENMARK"),
                    ("Djibouti", "DJIBOUTI"),
                    ("Dominica", "DOMINICA"),
                    ("Dominican Republic", "DOMINICAN_REPUBLIC"),
                    ("East Timor", "EAST_TIMOR"),
                    ("Ecuador", "ECUADOR"),
                    ("Egypt", "EGYPT"),
                    ("El Salvador", "EL_SALVADOR"),
                    ("Equatorial Guinea", "EQUATORIAL_GUINEA"),
                    ("Eritrea", "ERITREA"),
                    ("Estonia", "ESTONIA"),
                    ("Ethiopia", "ETHIOPIA"),
                    ("Fiji", "FIJI"),
                    ("Finland", "FINLAND"),
                    ("France", "FRANCE"),
                    ("Gabon", "GABON"),
                    ("Gambia", "GAMBIA"),
                    ("Georgia", "GEORGIA"),
                    ("Germany", "GERMANY"),
                    ("Ghana", "GHANA"),
                    ("Greece", "GREECE"),
                    ("Grenada", "GRENADA"),
                    ("Guatemala", "GUATEMALA"),
                    ("Guinea", "GUINEA"),
                    ("Guinea-Bissau", "GUINEA_BISSAU"),
                    ("Guyana", "GUYANA"),
                    ("Haiti", "HAITI"),
                    ("Honduras", "HONDURAS"),
                    ("Hungary", "HUNGARY"),
                    ("Iceland", "ICELAND"),
                    ("India", "INDIA"),
                    ("Indonesia", "INDONESIA"),
                    ("Iran", "IRAN"),
                    ("Iraq", "IRAQ"),
                    ("Ireland {Republic}", "IRELAND"),
                    ("Israel", "ISRAEL"),
                    ("Italy", "ITALY"),
                    ("Ivory Coast", "IVORY_COAST"),
                    ("Jamaica", "JAMAICA"),
                    ("Japan", "JAPAN"),
                    ("Jordan", "JORDAN"),
                    ("Kazakhstan", "KAZAKHSTAN"),
                    ("Kenya", "KENYA"),
                    ("Kiribati", "KIRIBATI"),
                    ("Korea North", "KOREA_NORTH"),
                    ("Korea South", "KOREA_SOUTH"),
                    ("Kosovo", "KOSOVO"),
                    ("Kuwait", "KUWAIT"),
                    ("Kyrgyzstan", "KYRGYZSTAN"),
                    ("Laos", "LAOS"),
                    ("Latvia", "LATVIA"),
                    ("Lebanon", "LEBANON"),
                    ("Lesotho", "LESOTHO"),
                    ("Liberia", "LIBERIA"),
                    ("Libya", "LIBYA"),
                    ("Liechtenstein", "LIECHTENSTEIN"),
                    ("Lithuania", "LITHUANIA"),
                    ("Luxembourg", "LUXEMBOURG"),
                    ("Macedonia", "MACEDONIA"),
                    ("Madagascar", "MADAGASCAR"),
                    ("Malawi", "MALAWI"),
                    ("Malaysia", "MALAYSIA"),
                    ("Maldives", "MALDIVES"),
                    ("Mali", "MALI"),
                    ("Malta", "MALTA"),
                    ("Marshall Islands", "MARSHALL_ISLANDS"),
                    ("Mauritania", "MAURITANIA"),
                    ("Mauritius", "MAURITIUS"),
                    ("Mexico", "MEXICO"),
                    ("Micronesia", "MICRONESIA"),
                    ("Moldova", "MOLDOVA"),
                    ("Monaco", "MONACO"),
                    ("Mongolia", "MONGOLIA"),
                    ("Montenegro", "MONTENEGRO"),
                    ("Morocco", "MOROCCO"),
                    ("Mozambique", "MOZAMBIQUE"),
                    ("Myanmar, {Burma}", "MYANMAR_BURMA"),
                    ("Namibia", "NAMIBIA"),
                    ("Nauru", "NAURU"),
                    ("Nepal", "NEPAL"),
                    ("Netherlands", "NETHERLANDS"),
                    ("New Zealand", "NEW_ZEALAND"),
                    ("Nicaragua", "NICARAGUA"),
                    ("Niger", "NIGER"),
                    ("Nigeria", "NIGERIA"),
                    ("Norway", "NORWAY"),
                    ("Oman", "OMAN"),
                    ("Pakistan", "PAKISTAN"),
                    ("Palau", "PALAU"),
                    ("Panama", "PANAMA"),
                    ("Papua New Guinea", "PAPUA_NEW_GUINEA"),
                    ("Paraguay", "PARAGUAY"),
                    ("Peru", "PERU"),
                    ("Philippines", "PHILIPPINES"),
                    ("Poland", "POLAND"),
                    ("Portugal", "PORTUGAL"),
                    ("Qatar", "QATAR"),
                    ("Romania", "ROMANIA"),
                    ("Russian Federation", "RUSSIAN_FEDERATION"),
                    ("Rwanda", "RWANDA"),
                    ("St Kitts & Nevis", "ST_KITTS_AND_NEVIS"),
                    ("St Lucia", "ST_LUCIA"),
                    (
                        "Saint Vincent & the Grenadines",
                        "SAINT_VINCENT_AND_THE_GRENADINES",
                    ),
                    ("Samoa", "SAMOA"),
                    ("San Marino", "SAN_MARINO"),
                    ("Sao Tome & Principe", "SAO_TOME_AND_PRINCIPE"),
                    ("Saudi Arabia", "SAUDI_ARABIA"),
                    ("Senegal", "SENEGAL"),
                    ("Serbia", "SERBIA"),
                    ("Seychelles", "SEYCHELLES"),
                    ("Sierra Leone", "SIERRA_LEONE"),
                    ("Singapore", "SINGAPORE"),
                    ("Slovakia", "SLOVAKIA"),
                    ("Slovenia", "SLOVENIA"),
                    ("Solomon Islands", "SOLOMON_ISLANDS"),
                    ("Somalia", "SOMALIA"),
                    ("South Africa", "SOUTH_AFRICA"),
                    ("South Sudan", "SOUTH_SUDAN"),
                    ("Spain", "SPAIN"),
                    ("Sri Lanka", "SRI_LANKA"),
                    ("Sudan", "SUDAN"),
                    ("Suriname", "SURINAME"),
                    ("Swaziland", "SWAZILAND"),
                    ("Sweden", "SWEDEN"),
                    ("Switzerland", "SWITZERLAND"),
                    ("Syria", "SYRIA"),
                    ("Taiwan", "TAIWAN"),
                    ("Tajikistan", "TAJIKISTAN"),
                    ("Tanzania", "TANZANIA"),
                    ("Thailand", "THAILAND"),
                    ("Togo", "TOGO"),
                    ("Tonga", "TONGA"),
                    ("Trinidad & Tobago", "TRINIDAD_AND_TOBAGO"),
                    ("Tunisia", "TUNISIA"),
                    ("Turkey", "TURKEY"),
                    ("Turkmenistan", "TURKMENISTAN"),
                    ("Tuvalu", "TUVALU"),
                    ("Uganda", "UGANDA"),
                    ("Ukraine", "UKRAINE"),
                    ("United Arab Emirates", "UNITED_ARAB_EMIRATES"),
                    ("United Kingdom", "UNITED_KINGDOM"),
                    ("United States", "UNITED_STATES"),
                    ("Uruguay", "URUGUAY"),
                    ("Uzbekistan", "UZBEKISTAN"),
                    ("Vanuatu", "VANUATU"),
                    ("Vatican City", "VATICAN_CITY"),
                    ("Venezuela", "VENEZUELA"),
                    ("Vietnam", "VIETNAM"),
                    ("Yemen", "YEMEN"),
                    ("Zambia", "ZAMBIA"),
                    ("Zimbabwe", "ZIMBABWE"),
                ],
                max_length=30,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="currency",
            field=models.CharField(
                blank=True,
                choices=[("USD", "USD"), ("Euro", "EURO")],
                max_length=4,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
