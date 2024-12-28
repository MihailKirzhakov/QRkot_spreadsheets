from datetime import datetime

from app.models.base import InvestmentBaseModel


def invest_donations(
    target: InvestmentBaseModel,
    sources: list[InvestmentBaseModel]
) -> list[InvestmentBaseModel]:
    changed_sources = []
    for source in sources:
        investment_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        for item in (source, target):
            item.invested_amount += investment_amount
            if item.full_amount == item.invested_amount:
                item.fully_invested = True
                item.close_date = datetime.now()
        changed_sources.append(source)
        if target.fully_invested:
            break
    return changed_sources
