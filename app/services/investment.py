# C:\Dev\cat_charity_fund\app\services\investment.py
from datetime import datetime
from typing import Union

from app.constants.constants import ConstantNumbers
from app.schemas.charityproject import CharityProjectDB
from app.models.donation import Donation
from app.models import CharityProject


def invest_donations(
    donation_or_project: Union[Donation, CharityProjectDB],
    targets: list[Union[CharityProject, Donation]]
):
    remaining_donation_amount = donation_or_project.full_amount
    invested_amount = 0

    for target in targets:
        if remaining_donation_amount <= 0:
            break

        need_donation = target.full_amount - target.invested_amount
        if need_donation <= remaining_donation_amount:
            target.invested_amount += need_donation
            invested_amount += need_donation
            remaining_donation_amount -= need_donation
        else:
            target.invested_amount += remaining_donation_amount
            invested_amount += remaining_donation_amount
            remaining_donation_amount = 0

        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()

    donation_or_project.invested_amount = invested_amount
    if remaining_donation_amount == 0:
        donation_or_project.close_date = datetime.now()
        donation_or_project.fully_invested = True

    return donation_or_project
