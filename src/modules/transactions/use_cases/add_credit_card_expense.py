from datetime import date
from pydantic import BaseModel, UUID4
from modules.transactions.core.interfaces.credit_card_repository import ICreditCardRepository
from modules.transactions.core.services.installment_generator import InstallmentGenerator
from modules.users.core.entities.value_objects import ExceptionDomain

class AddCreditCardExpenseInputDTO(BaseModel):
    user_id: UUID4
    credit_card_id: UUID4
    title: str
    total_amount: float
    total_installments: int
    first_due_date: date

class AddCreditCardExpense:
    """O Caso de Uso Central: Une a Web, o Motor Matemático e o Banco de Dados."""
    def __init__(self, repo: ICreditCardRepository):
        self.repo = repo

    def execute(self, dto: AddCreditCardExpenseInputDTO) -> None:
        # Segurança Básica (Avançado: Verificar antes no banco se o card_id pertence ao user_id real!)
        card = self.repo.find_card_by_id(str(dto.credit_card_id))
        if not card or card.user_id != dto.user_id:
            raise ExceptionDomain("Cartão Inexistente ou usuário não autorizado.")
            
        # O Motor purificado cospe as classes filhas prontas pro banco
        installments = InstallmentGenerator.generate(
            user_id=dto.user_id,
            credit_card_id=dto.credit_card_id,
            title=dto.title,
            total_amount=dto.total_amount,
            total_installments=dto.total_installments,
            first_due_date=dto.first_due_date
        )
        
        # Repassa o Lote de Dados de uma Vez Para a gaveta correta do Banco (Bulk Insert)
        self.repo.save_transactions(installments)
