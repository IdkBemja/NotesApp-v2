from app.services.database import session, BlacklistedToken

def is_token_blacklisted(token):
    """Verifica si un token está en la lista negra."""
    blacklisted = session.query(BlacklistedToken).filter_by(token=token).first()
    return blacklisted is not None