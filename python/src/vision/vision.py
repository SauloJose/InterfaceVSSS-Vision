import unidecode
#Código de visão aqui
str = 'Olá Imrão'

str_cor=  unidecode.unidecode(str).lower()

print(str_cor)