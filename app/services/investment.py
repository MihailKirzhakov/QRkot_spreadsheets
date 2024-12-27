from datetime import datetime

from app.models.base import InvestmentBaseModel


def invest_donations(
    donation_or_project: InvestmentBaseModel,
    targets: list
):
    remaining_donation_amount = donation_or_project.full_amount
    for target in targets:
        need_donation = target.full_amount - target.invested_amount
        donation_amount = min(need_donation, remaining_donation_amount)
        for obj in (target, donation_or_project):
            obj.invested_amount += donation_amount
        remaining_donation_amount -= donation_amount
        if target.invested_amount >= target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
    if remaining_donation_amount == 0:
        donation_or_project.close_date = datetime.now()
        donation_or_project.fully_invested = True
    return donation_or_project