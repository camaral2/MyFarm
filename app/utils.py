from passlib.context import CryptContext

pws_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def has_password(password: str):
    return pws_context.hash(password)

def verify(plain_password, hashed_password):
    return pws_context.verify(plain_password, hashed_password)

def paging_set_valid(numpag):
    page = numpag
    if(page<1): page =1
    return page-1