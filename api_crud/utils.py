#common utils
import json
import mimetypes
import random
import re
import string
import urllib
import uuid
from datetime import datetime, timedelta
from io import BytesIO
from typing import Tuple

from django.core.files import File
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy
from rest_framework import status
from rest_framework.exceptions import APIException

from api_crud import settings
from api_crud.constants import (
    ABBR_STATES,
    ASSOCIATIONS,
    FILING_TYPE,
    IMPACT_CHOICES,
    IMPACT_CHOICES_ORDER,
    IMPACT_QUARTERS,
    INCOME_CHOICE,
    INDUSTRY,
    STATES,
)
from api_crud.local_settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM


def label_to_id_transform(id_to_label):
    return {value.lower(): key for key, value in id_to_label}


def get_industry_id(label: str) -> int:
    label_to_id = label_to_id_transform(INDUSTRY)
    return label_to_id.get(label.lower())

def get_estimate(employees_2020, employees_2021):
    return employees_2020 * 5000 + employees_2021 * 21000

# only user with these groups can login
def is_member(user):
    return user.groups.filter(
        name__in=['Customer', 'CSC User', 'CSC Team Lead', 'CSC Manager', 'CPA', 'Super Admin', 'Executive']).exists()

# check whether user is customer
def is_customer(user):
    return user.groups.filter(name__in=['Customer']).exists()

def is_csc(user):
    return user.groups.filter(name__in=['CSC User', 'CSC Team Lead', 'CSC Manager']).exists()

#has csc portal permissions
def has_csc(user):
    return user.groups.filter(name__in=['CSC User', 'CSC Team Lead', 'CSC Manager', 'Super Admin']).exists()

# check whether user is CSC user
def is_csc_user(user):
    return user.groups.filter(name__in=['CSC User']).exists()

# check whether user is CSC team lead
def is_csc_team_lead(user):
    return user.groups.filter(name__in=['CSC Team Lead']).exists()

def is_csc_manager(user):
    return user.groups.filter(name__in=['CSC Manager']).exists()

# check whether user is cpa
def is_cpa(user):
    return user.groups.filter(name__in=['CPA']).exists()

# check whether user is super admin
def is_super_admin(user):
    return user.groups.filter(name__in=['Super Admin']).exists()

# check whether user is executive
def is_executive(user):
    return user.groups.filter(name__in=['Executive']).exists()

def has_da_user(user):
    return user.groups.filter(name__in=['Data Aggregator', 'Data Aggregator Manager','Super Admin']).exists()

def is_da_user(user):
    return user.groups.filter(name__in=['Data Aggregator', 'Data Aggregator Manager']).exists()

def is_law_admin(user):
    return user.groups.filter(name__in=['Law Admin']).exists()

def get_941_association(quarter):
    if quarter == 1:
        return 2
    elif quarter == 2:
        return 3
    elif quarter == 3:
        return 4
    elif quarter == 4:
        return 5
    elif quarter == 5:
        return 6
    elif quarter == 6:
        return 7
    elif quarter == 7:
        return 8
    elif quarter == 8:
        return 9
    elif quarter == 9:
        return 10
    elif quarter == 10:
        return 11
    elif quarter == 11:
        return 12
    elif quarter == 12:
        return 13

    return 1

def get_943_association(year):
    if year == 1:
        return 16
    elif year == 2:
        return 17
    elif year == 3:
        return 18

    return 1

def get_payroll_association(upload_month):
    if upload_month == 1:
        return 20
    elif upload_month == 2:
        return 21
    elif upload_month == 3:
        return 22
    elif upload_month == 4:
        return 23
    elif upload_month == 5:
        return 24
    elif upload_month == 6:
        return 25
    elif upload_month == 7:
        return 26
    elif upload_month == 8:
        return 27
    elif upload_month == 9:
        return 28
    elif upload_month == 10:
        return 29
    elif upload_month == 11:
        return 30
    elif upload_month == 12:
        return 31
    elif upload_month == 13:
        return 32
    elif upload_month == 14:
        return 33
    elif upload_month == 15:
        return 34
    elif upload_month == 16:
        return 35
    elif upload_month == 17:
        return 36
    elif upload_month == 18:
        return 37
    elif upload_month == 19:
        return 38
    elif upload_month == 20:
        return 39
    elif upload_month == 21:
        return 40
    elif upload_month == 22:
        return 41
    elif upload_month == 23:
        return 42
    elif upload_month == 24:
        return 43

    return 1


def get_eb_association(upload_month):
    if upload_month == 1:
        return 50
    elif upload_month == 2:
        return 51
    elif upload_month == 3:
        return 52
    elif upload_month == 4:
        return 53
    elif upload_month == 5:
        return 54
    elif upload_month == 6:
        return 55
    elif upload_month == 7:
        return 56
    elif upload_month == 8:
        return 57
    elif upload_month == 9:
        return 58
    elif upload_month == 10:
        return 59
    elif upload_month == 11:
        return 60
    elif upload_month == 12:
        return 61
    elif upload_month == 13:
        return 62
    elif upload_month == 14:
        return 63
    elif upload_month == 15:
        return 64
    elif upload_month == 16:
        return 65
    elif upload_month == 17:
        return 66
    elif upload_month == 18:
        return 67
    elif upload_month == 19:
        return 68
    elif upload_month == 20:
        return 69
    elif upload_month == 21:
        return 70
    elif upload_month == 22:
        return 71
    elif upload_month == 23:
        return 72
    elif upload_month == 24:
        return 73

    return 1

def get_pnl_association(quarter):
    if quarter == 1:
        return 80
    elif quarter == 2:
        return 81
    elif quarter == 3:
        return 82
    elif quarter == 4:
        return 83
    elif quarter == 5:
        return 84
    elif quarter == 6:
        return 85
    elif quarter == 7:
        return 86
    elif quarter == 8:
        return 87
    elif quarter == 9:
        return 88
    elif quarter == 10:
        return 89
    elif quarter == 11:
        return 90
    elif quarter == 12:
        return 91

    return 1

def get_ppp_association(pround):
    if pround == 1:
        return 100
    elif pround == 2:
        return 101

    return 1

# from https://irqa.s3.amazonaws.com/1265/941/bb2aa41963cc432ab8dc21bf0d54277b.png?AWSAccessKeyId
# to 1265/941/bb2aa41963cc432ab8dc21bf0d54277b.png
def get_s3_file(input):
    tmp = input.replace('https://', '')
    i = tmp.find('/')
    if i != -1:
        tmp1 = tmp[i+1:]

        j = tmp1.find('?')
        if j != -1:
            tmp2 = tmp1[0:j]

            k = tmp2.find('.')
            if k != -1:
                tmp3 = tmp2[k+1:]
            return tmp2, tmp3

    return '', ''


def get_new_file(subfolder, association, ext):
    d = dict(ASSOCIATIONS)
    tmp = d[association].replace(' ', '-')
    return subfolder + '/' +tmp + '.' + ext


def download_file(fl_path, filename):
    fl = urllib.request.urlopen(fl_path)
    mime_type = fl.info().get_content_type()
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


# generate random string for password etc
def random_string(size=12, chars=string.ascii_uppercase + string.digits):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(size))

def get_company_industry(industry):
    d = dict(INDUSTRY)

    if industry in d:
        return d[industry]

    return None

def get_company_revenue(industry):
    d = dict(INCOME_CHOICE)

    if industry in d:
        return d[industry]

    return None

def get_company_type(industry):
    d = dict(FILING_TYPE)

    if industry in d:
        return d[industry]

    return None

def get_state(state):
    d = dict(ABBR_STATES)

    if state in d:
        return d[state]

    return None

def get_choices(choices):
    out = ''

    d = dict(IMPACT_CHOICES)

    for c in choices:
        out = out + d[c] + "; "

    return out

def ordered_choices():
    impact_choices = list(IMPACT_CHOICES)
    impact_choices.sort(key=lambda x: dict(IMPACT_CHOICES_ORDER)[x[0]])

    return tuple(impact_choices)

def get_quarters(quarters):
    out = ''
    d = dict(IMPACT_QUARTERS)

    for c in quarters:
        out = out + d[c] + "; "

    return out

#hubspot only eats Yes/No
def get_yes_no(input):
    if input:
        return "Yes"
    return "No"


def is_number(s):
    if s is None:
        return False

    try:
        float(s)
        return True
    except ValueError:
        return False


class AssociationMap:
    _association_map = dict({})

    def __init__(self):
        for association in ASSOCIATIONS:
            self._association_map[str(association[0])] = association[1]

    def get_associated_file_name(self, assoication_id: int) -> str:
        return self._association_map.get(str(assoication_id), None)


def get_completion_date(selected_date, days):
    days_to_add = days-1
    completion_date = selected_date

    if not selected_date:
        return ""

    while days_to_add > 0:
        completion_date = completion_date + timedelta(days=1)
        weekday = completion_date.weekday()
        if weekday >= 5:
            continue
        days_to_add -= 1
    completion_date = completion_date.strftime('%m/%d/%Y')
    return completion_date


class EmptyResponse(APIException):
    """
    APIException with empty payload
    """
    status_code = status.HTTP_200_OK
    default_detail = gettext_lazy('')

    def __init__(self, detail=None, code=None):
        self.detail = {}

class EmptyListResponse(APIException):
    """
    APIException with empty payload
    """
    status_code = status.HTTP_200_OK
    default_detail = gettext_lazy('')

    def __init__(self, detail=None, code=None):
        self.detail = []

def get_queryset(klass):
    """
    Copy&paste from django.shortcuts._get_queryset() to avoid
    importing non-public method
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass

def get_object_or_return_empty_response(klass, *args, **kwargs):
    """
    Use get() to return an object, or raise an EpmtyResponse exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_return_empty_response() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise EmptyResponse()

def get_list_or_return_empty_response(klass, *args, **kwargs):
    """
    Use filter() to return a list of objects, or raise an EpmtyResponse exception if
    the list is empty.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the filter() query.
    """
    queryset = get_queryset(klass)
    if not hasattr(queryset, "filter"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_list_or_return_empty_response() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        raise EmptyListResponse()
    return obj_list

def get_year_and_quarter_from_payroll_quarter(payroll_quarter: int) -> Tuple[int, int]:
    year_and_quarter_map = {
        1: (2019, 1),
        2: (2019, 2),
        3: (2019, 3),
        4: (2019, 4),
        5: (2020, 1),
        6: (2020, 2),
        7: (2020, 3),
        8: (2020, 4),
        9: (2021, 1),
        10: (2021, 2),
        11: (2021, 3),
        12: (2021, 4)
    }

    return year_and_quarter_map.get(payroll_quarter)


def get_association_id(association_label: str) -> int:
    """Return the ID associated with the given association label.

    :param association_label: A string representing the label associated with the association ID.
    :return: An integer representing the ID of the association.
    """
    label_to_id = {value.lower(): key for key, value in ASSOCIATIONS}
    return label_to_id.get(association_label.lower())

def is_ein_valid(ein: str) -> bool:
    """Check, if EIN is written in the correct format: XX-XXXXXXX"""
    pattern = re.compile(r"^\d{2}-\d{7}$")
    if re.match(pattern, ein):
        return True

    return False
