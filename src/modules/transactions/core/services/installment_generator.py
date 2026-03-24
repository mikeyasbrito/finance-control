import uuid
from datetime import date
from modules.transactions.core.entities.credit_card_transaction import CreditCardTransaction

class InstallmentGenerator:
    """Domain Service responsável por fatiar uma compra em múltiplas parcelas matemáticas ao longo do tempo."""

    @staticmethod
    def _add_months(sourcedate: date, months: int) -> date:
        import calendar
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @staticmethod
    def generate(
        user_id: uuid.UUID,
        credit_card_id: uuid.UUID,
        title: str,
        total_amount: float,
        total_installments: int,
        first_due_date: date
    ) -> list[CreditCardTransaction]:
        
        installments = []
        # Arredonda valor base para 2 casas decimais (Ex: 100.0 / 3 = 33.33)
        base_amount = round(total_amount / total_installments, 2)
        total_generated = 0.0
        
        for i in range(1, total_installments + 1):
            # A classe de cálculo nativa garante que saltar de Janeiro 31 para Feveireiro retorne Dia 28!
            current_date = InstallmentGenerator._add_months(first_due_date, i - 1)
            
            # Ajustando a falha sistêmica dos centavos: A última fatura sempre paga a diferença inteira final.
            if i == total_installments:
                current_amount = round(total_amount - total_generated, 2)
            else:
                current_amount = base_amount
                
            total_generated += current_amount
            installment_title = f"{title} ({i}/{total_installments})"
            
            tx = CreditCardTransaction(
                user_id=user_id,
                credit_card_id=credit_card_id,
                title=installment_title,
                amount=current_amount,
                installment_number=i,
                total_installments=total_installments,
                date=current_date
            )
            installments.append(tx)
            
        return installments
