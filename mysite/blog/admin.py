from django.contrib import admin
from blog.models import Post, Comment, SolCamb, appointment, ProdID, Book, ProgramaConv, PruebaMod, PruebaTabla, OrdenProg, DetalleProg, ProdReal, Maquinas, Turnos


# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(SolCamb)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(appointment)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(ProdID)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(Book)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(ProgramaConv)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(PruebaMod)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(PruebaTabla)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(OrdenProg)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(DetalleProg)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(ProdReal)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(Maquinas)#Cuando se agregan estos hay que aplicar el migrate
admin.site.register(Turnos)#Cuando se agregan estos hay que aplicar el migrate
