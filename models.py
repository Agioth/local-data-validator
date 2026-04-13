from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class CompanyModel(BaseModel):
    # Campos básicos
    name: str
    address: Optional[str] = "Não informado"
    phone: str
    rating: float = 0.0
    reviews_count: int = 0
    owner_photos: int = 0
    is_claimed: bool = False
    
    # Campo calculado para o seu "Scoring de Empregabilidade"
    @property
    def leads_quality_score(self) -> int:
        score = 100
        # Se não tem o 9º dígito ou é fixo, perde pontos de "modernidade"
        clean_phone = re.sub(r'\D', '', self.phone)
        if len(clean_phone) < 11:
            score -= 30
        # Se o dono não tem fotos, perde pontos de "presença digital"
        if self.owner_photos == 0:
            score -= 40
        return max(score, 0)

    @field_validator('phone')
    @classmethod
    def clean_phone_number(cls, v: str) -> str:
        # Remove tudo que não é número
        digits = re.sub(r'\D', '', v)
        if not digits:
            return "Sem Telefone"
        return digits

# Teste simples para ver a blindagem funcionando
if __name__ == "__main__":
    test_data = {
        "name": "Pet Shop Castanhal",
        "phone": "(91) 3721-1234", # Telefone fixo (antigo)
        "owner_photos": 0,
        "is_claimed": False
    }
    
    empresa = CompanyModel(**test_data)
    print(f"Empresa: {empresa.name}")
    print(f"Telefone Limpo: {empresa.phone}")
    print(f"Score de Lead: {empresa.leads_quality_score}/100")