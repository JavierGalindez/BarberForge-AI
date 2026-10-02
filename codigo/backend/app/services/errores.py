class ErrorDominio(Exception):
    """Error de negocio. main.py lo traduce a una respuesta HTTP."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class NoEncontrado(ErrorDominio):
    pass


class Conflicto(ErrorDominio):
    pass


class DatosInvalidos(ErrorDominio):
    pass


class PermisoDenegado(ErrorDominio):
    pass


class CredencialesInvalidas(ErrorDominio):
    pass
