from django.core.exceptions import ValidationError


# validar campo convocatoria de tabla compras
def validate_compras_convocatoria(value):
    if value > 0:
        return True
    else:
        raise ValidationError("Este campo no puede contener valores negativos")

# validar campo tipo_sc de tabla solicitante_compra
def validate_solicitante_compra_tipo_sc(value):
    if value == "li" or value == "in":
        return True
    else:
        raise ValidationError("Tipo de solicitante no encontrado")