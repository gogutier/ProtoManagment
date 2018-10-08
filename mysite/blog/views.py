from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post,Comment,SolCamb, appointment, CargaCSV, OCImportacion, ProdID, Book, PruebaMod, PruebaTabla, OrdenProg, DetalleProg, ProdReal, Maquinas, Turnos
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from blog.forms import PostForm, CommentForm, SolCambForm, ContactForm, AppointmentForm, OCImportacionForm, ProdIDForm, BookFormset, BookModelFormset, PruebaModForm
from django.views.generic import (TemplateView,ListView,CreateView,DetailView, UpdateView, DeleteView)
import csv
from io import StringIO

#VIEWS ES DONDE SE PUEDE PROGRAMR EN PYTHON?
#views functions take as input: HTTPRESPONSE objects, and returns HTTPRESpose object (html output)

class OrdenProgDetailView(DetailView):
    context_object_name = 'ordenprog'
    model = OrdenProg
    maquinas = Maquinas.objects.all()

    ordenes = OrdenProg.objects.all()
    detallesProg = DetalleProg.objects.all()



    def actualizadatos(self, pk):
        #referencia = OrdenProg.objects.filter(pk=pk[0])#ojo tmabién puede ser con el get. ahí hay que poner el [0] ya que no acepta más de un resultado
        referencia = OrdenProg.objects.get(pk=pk)
        detalles = DetalleProg.objects.filter(programma = referencia)

        for produccionprogramada in detalles:
            print("hola")
            for real in ProdReal.objects.filter(orderId = produccionprogramada.orderId, datefinajustada=produccionprogramada.datefinajustada):
                produccionprogramada.completo_unidades = str(real.qProd)+"/"+str(produccionprogramada.qIn)
                produccionprogramada.save()
            #busco si en las producciones reales hay alguna que coincida en orderID, máquina y fecha-Turno

        '''
        for ref in referencia## por cada orden programada que tenga el pk que se está consultando

            for real in detallesProg.filter(orderId = ref.orderId): #por cada producción real que tenga el mismo order id (y máquina) que se está consultando
            ref
            #real.qProd='llenoooo'
            #real.save()

            print("actualizado: " + real.orderId )
            '''



    def get_context_data(self, **kwargs):
        """
        This has been overridden to add `car` to the template context,
        now you can use {{ car }} within the template
        """
        pk = self.kwargs['pk']# this is the primary key from your URL
        # your other code

        print(pk)

        #Aquí calcula indicadores programado vs real y los guarda en la base de datos, para que después del detailview pueda mostrarlos como dato.

        self.actualizadatos(pk)

        context = super().get_context_data(**kwargs)
        context['detalleprog'] = DetalleProg.objects.all()#.filter(published_date__isnull=True).order_by('-published_date')
        context['progreal'] = ProdReal.objects.all()#.filter(published_date__isnull=True).order_by('-published_date')
        context['maquinas'] = Maquinas.objects.all()#.filter(published_date__isnull=True).order_by('-published_date')
        context['turnos'] = Turnos.objects.all()#.filter(published_date__isnull=True).order_by('-published_date')
        #context['maquinas'] = maquinas
        return context





def res_conv_v2(request):
    template_name = 'blog/resumenconv.html'
    ordenes = OrdenProg.objects.all()
    detallesProg = DetalleProg.objects.all()

    ##Acá calcula los indicadores para cada Programa de producción?


    return render(request, template_name, {'ordenes':ordenes, "detallesProg": detallesProg})

class ResConvView(ListView):
    model = OrdenProg


def carga_prod_real(request):
    template_name = 'blog/cargaprodreal.html'
    prodsreales = ProdReal.objects.all()
    if request.method == "POST":
        form = PruebaModForm(request.POST)
        if form.is_valid():
            datocrudo=form.cleaned_data["ultrafile"]
            print("datocrudo.clean: " + datocrudo)
        else:
            datocrudo=form.data["ultrafile"]
            datoprocesado=datocrudo.split(",;,")
            print("datoprocesado1:")
            print(datoprocesado)
            for i in range (len(datoprocesado)):
                datoprocesado[i]=datoprocesado[i].split(",")
            print(datoprocesado)
            ####### identifica las columnas y crea los objetos que me interesanself.
            colCliente = None
            colOrderId = None
            colPadron = None
            colDatefin = None
            colDatefinajust = None
            colTurno = None
            colUnisprod = None
            colMaquina = None

            for i in range(len(datoprocesado[0])):
                if datoprocesado[0][i] == "Cliente":
                    #print("columna creación en: " + str(i))
                    colCliente = i

                if datoprocesado[0][i] == "No. Orden":
                    #print("columna transaction en: " + str(i))
                    colOrderId = i

                if datoprocesado[0][i] == "ID Especificacion":
                    #print("columna transaction en: " + str(i))
                    colPadron = i

                if datoprocesado[0][i] == "Fecha Hora de termino":
                    #print("columna transaction en: " + str(i))
                    colDatefin = i

                if datoprocesado[0][i] == "Fecha termino ajustada":
                    #print("columna transaction en: " + str(i))
                    colDatefinajust = i


                if datoprocesado[0][i] == "Turno":
                    #print("columna transaction en: " + str(i))
                    colTurno = i



                if datoprocesado[0][i] == "Laminas Producidas":
                    #print("columna transaction en: " + str(i))
                    colUnisprod = i


                if datoprocesado[0][i] == "Maquina":
                    #print("columna transaction en: " + str(i))
                    colMaquina= i


            '''
            #ejemplo

            obj, created = Person.objects.get_or_create(
                first_name='John',
                last_name='Lennon',
                defaults={'birthday': date(1940, 10, 9)},
            )
            '''

            for i in range(1,len(datoprocesado)):
                #if i==1:
                #    Reciencreado=ProdReal.objects.get_or_create(cliente=datoprocesado[i][colCliente], orderId=datoprocesado[i][colOrderId], orderIdPrev="Primero", orderIdPost=datoprocesado[i+1][colOrderId])
                #elif i==len(datoprocesado):
                #    Reciencreado=ProdReal.objects.get_or_create(cliente=datoprocesado[i][colCliente], orderId=datoprocesado[i][colOrderId], orderIdPrev=datoprocesado[i-1][colOrderId], orderIdPost=datoprocesado[i+1][colOrderId])
                #else:
                ProdReal.objects.get_or_create(cliente=datoprocesado[i][colCliente], orderId=datoprocesado[i][colOrderId], orderIdPrev="pendiente", orderIdPost="Final", datefin=datoprocesado[i][colDatefin], datefinajustada=datoprocesado[i][colDatefinajust], turno=datoprocesado[i][colTurno], qProd=datoprocesado[i][colUnisprod], maquina=datoprocesado[i][colMaquina])
            #################


    else:
        form = PruebaModForm()

    return render(request, template_name, {'form':form})


def carga_prog(request):
    pruebamods = PruebaMod.objects.all()
    posts= "HOLA Q ASE"
    template_name = 'blog/cargaprog.html'

    if request.method == "POST":
        form = PruebaModForm(request.POST)
        if form.is_valid():


            datocrudo=form.cleaned_data["ultrafile"]
            datoprocesado=datocrudo.split(";")

            PruebaTabla.objects.create(item1=datoprocesado[0],item2=datoprocesado[1],item3=datoprocesado[2])

            post = form.save(commit=False)

            post.save()

        else:
            datocrudo=form.data["ultrafile"]
            '''
            f = StringIO(datocrudo)
            reader = list(csv.reader(f, delimiter=','))
            print("hola")
            for row in reader:
                print('\t'.join(row))
                print("siguiente linea")
            #print(reader)
            '''
            datoprocesado=datocrudo.split(",;,")
            print("datoprocesado1:")
            print(datoprocesado)
            print("Largo: " + str(len(datoprocesado)))
            for i in range (len(datoprocesado)):
                datoprocesado[i]=datoprocesado[i].split(",")

            print("datoprocesado2:")
            print(datoprocesado)
            '''
            print(datoprocesado[0])
            print("otro metodo:")

            print ((str.strip, s_inner.split(',')) for s_inner in datocrudo.split(";"))
            print("tercer metodo:")
            x = csv.reader(datocrudo)
            list(x)
            '''
            ####### identifica las columnas y crea los objetos que me interesanself.
            colFecha = None
            colTransindex = None
            colHorini = None
            colHorfin = None






            for i in range(len(datoprocesado[0])):
                if datoprocesado[0][i] == "CREACION_PROGRAMACION":
                    print("columna creación en: " + str(i))
                    colFecha = i

                if datoprocesado[0][i] == "TRANSACTIONINDEX":
                    print("columna transaction en: " + str(i))
                    colTransindex = i

                if datoprocesado[0][i] == "Horizonteini":
                    print("columna Horizonteini en: " + str(i))
                    colHorini = i

                if datoprocesado[0][i] == "Horizontefin":
                    print("columna Horizontefin en: " + str(i))
                    colHorfin= i

            '''
            #ejemplo

            obj, created = Person.objects.get_or_create(
                first_name='John',
                last_name='Lennon',
                defaults={'birthday': date(1940, 10, 9)},
            )
            '''

            OrdenProg.objects.get_or_create(fecha_programa=datoprocesado[1][colFecha], transaction_index=datoprocesado[1][colTransindex], horizonteini=datoprocesado[1][colHorini], horizontefin=datoprocesado[1][colHorfin] )

            #################
            #################
            ## guardo el objeto DetalleProg por cada fila de la tabla procesada

            colworkcenter = None
            colorderid = None
            coldateini = None
            coldatefin = None
            colqin = None
            colidprev = None
            colidpost = None
            coldatefinajust = None
            colturno = None


            print("Largo: " + str(len(datoprocesado[0])))
            for j in range(1,len(datoprocesado[0])):
                if datoprocesado[0][j] == "WORKCENTERID":
                    print("columna colworkcenter en: " + str(j))
                    colworkcenter = j
                if datoprocesado[0][j] == "ORDERID":
                    print("columna colorderid en: " + str(j))
                    colorderid = j
                if datoprocesado[0][j] == "SETUPSTARTDATE":
                    print("columna dateini en: " + str(j))
                    coldateini = j
                if datoprocesado[0][j] == "RUNENDDATE":
                    print("columna datefin en: " + str(j))
                    coldatefin = j
                if datoprocesado[0][j] == "QUANTITYIN":
                    print("columna qin en: " + str(j))
                    colqin = j
                if datoprocesado[0][j] == "Fecha Termino Ajustada":
                    print("columna datefinajust en: " + str(j))
                    coldatefinajust = j
                if datoprocesado[0][j] == "Turno":
                    print("columna turno en: " + str(j))
                    colturno = j
            print("Completado!!!!")

            for i in range(1,len(datoprocesado)):
                #try:
                    print(OrdenProg.objects.all())
                    print(datoprocesado[i])
                    if i==1:
                        DetalleProg.objects.get_or_create(programma=OrdenProg.objects.filter(fecha_programa=datoprocesado[1][colFecha], transaction_index=datoprocesado[1][colTransindex])[0],workcenter=datoprocesado[i][colworkcenter],orderId=datoprocesado[i][colorderid], dateini=datoprocesado[i][coldateini], datefin=datoprocesado[i][coldatefin],qIn=datoprocesado[i][colqin], orderIdPrev="Primero",orderIdPost="segundo", datefinajustada=datoprocesado[i][coldatefinajust] , turno=datoprocesado[i][colturno])

                    elif i==len(datoprocesado)-1:
                        DetalleProg.objects.get_or_create(programma=OrdenProg.objects.filter(fecha_programa=datoprocesado[1][colFecha], transaction_index=datoprocesado[1][colTransindex])[0],workcenter=datoprocesado[i][colworkcenter],orderId=datoprocesado[i][colorderid], dateini=datoprocesado[i][coldateini], datefin=datoprocesado[i][coldatefin],qIn=datoprocesado[i][colqin], orderIdPrev=datoprocesado[i-1][colorderid], orderIdPost="Final", datefinajustada=datoprocesado[i][coldatefinajust] , turno=datoprocesado[i][colturno], )

                    else:
                        DetalleProg.objects.get_or_create(programma=OrdenProg.objects.filter(fecha_programa=datoprocesado[1][colFecha], transaction_index=datoprocesado[1][colTransindex])[0],workcenter=datoprocesado[i][colworkcenter],orderId=datoprocesado[i][colorderid], dateini=datoprocesado[i][coldateini], datefin=datoprocesado[i][coldatefin],qIn=datoprocesado[i][colqin], datefinajustada=datoprocesado[i][coldatefinajust] , turno=datoprocesado[i][colturno], orderIdPrev=datoprocesado[i-1][colorderid], orderIdPost=datoprocesado[i+1][colorderid])


                #except:

                    #print("hola")



            #PruebaTabla.objects.create(item1="form no valido11 !!", item2=datoprocesado[0], item3=datoprocesado,)



    else:
        form = PruebaModForm()

    return render(request, template_name, {'form':form})




def prueba_ultimate(request):
    pruebamods = PruebaMod.objects.all()
    posts= "HOLA Q ASE"
    template_name = 'blog/pruebaultimate.html'
    redirec_field_name = 'blog/pruebaultimate.html'

    if request.method == "POST":
        form = PruebaModForm(request.POST)
        if form.is_valid():

            '''
            ##Ejemplo de cómo crear un objeto de otra clase al llenar el form (para hacer el parse el ultimatefile y generar filas de info productiva)
            ##Se llena form de producto y si la categoría no existe, se crea el objeto de una categoría nueva (model Category)
            if form.is_valid():
                c = form.cleaned_data["category"]
                category = Category.objects.filter(name=c).first()
                if not category:
                    category = Category.objects.create(name=c)
            product = form.save(commit=False)
            product.category = category
            product.save()

            '''
            datocrudo=form.cleaned_data["ultrafile"]
            datoprocesado=datocrudo.split(",")

            PruebaTabla.objects.create(item1=datoprocesado[0],item2=datoprocesado[1],item3=datoprocesado[2])




            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            #return redirect('post_detail', pk=post.pk)
    else:
        form = PruebaModForm()



    return render(request, template_name, {'pruebamods':pruebamods, 'posts':posts, 'form':form})



def create_book_with_authors(request):
    template_name = 'blog/create_with_author.html'
    if request.method == 'GET':
        bookform = BookModelForm(request.GET or None)
        formset = AuthorFormset(queryset=Author.objects.none())
    elif request.method == 'POST':
        bookform = BookModelForm(request.POST)
        formset = AuthorFormset(request.POST)
        if bookform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            book = bookform.save()
            for form in formset:
                # so that `book` instance can be attached.
                author = form.save(commit=False)
                author.book = book
                author.save()
            return redirect('blog:book_list')
    return render(request, template_name, {
        'bookform': bookform,
        'formset': formset,
    })

def create_book_model_form(request):
    template_name = 'blog/create_normal.html'
    heading_message = 'Model Formset Demo'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = BookModelFormset(queryset=Book.objects.none())
    elif request.method == 'POST':
        formset = BookModelFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # only save if name is present
                if form.cleaned_data.get('name'):
                    form.save()
            return redirect('book_list')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })




#Para el ejemplo de dynamic form creation
def create_book_normal(request):
    template_name = 'blog/create_normal.html'
    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    Book(name=name).save()
            # once all books are saved, redirect to book list view
            return redirect('book_normal')
            #return redirect('book_list')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })








def solcambiosss(request):

    return render(request, 'blog/solicitud_cambio.html')


def listaprodid(request):
    lista = ProdID.objects.all() #Tb podría haber sido filter
    context= {'lista_a_mostrar': lista}
    return render(request, 'blog/prodid_list.html', context)


class ProdIDListView(ListView):
    login_url = '/login/'
    #redirec_field_name = 'blog/post_detail.html'



    model = ProdID


    #redirect_field_name = 'blog/prodid_list.html'


    def get_queryset(self):
        return ProdID.objects.filter(published_date__isnull=True).order_by('-published_date')#sql query


def CargaCSV2(request):
    login_url = '/login/'
    redirec_field_name = 'blog/post_detail.html'
    with open("prueba2.csv") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            _, created = ProdID.objects.get_or_create(
                transactindex =row[0],
                plantid=row[1],
                workcenter=row[2],
                orderid=row[4],
                title=row[4]+row[2],
                #middle_name=row[2],
                )

    def get_queryset(self):
        return ProdID.objects.filter(published_date__isnull=True).order_by('-published_date')#sql query
            # creates a tuple of the new object or
            # current object and a boolean of if it was created
    lista = ProdID.objects.all() #Tb podría haber sido filter
    context= {'lista_a_mostrar': lista}
    return render(request, 'blog/prodid_list.html', context)





def CargaCSV1(request):
    login_url = '/login/'
    redirec_field_name = 'blog/post_detail.html'
    with open("prueba.csv") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            _, created = appointment.objects.get_or_create(
                title=row[0],
                text=row[1],
                #middle_name=row[2],
                )

    def get_queryset(self):
        return appointment.objects.filter(published_date__isnull=True).order_by('-published_date')#sql query
            # creates a tuple of the new object or
            # current object and a boolean of if it was created
    return render(request, 'blog/base.html')

def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})





def product(x,y):
    return x*y

def tomanombre():
    return SolCamb.objects.all()[:5]


class CreateOCIView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    #redirec_field_name = 'blog/post_detail.html'

    form_class = OCImportacionForm

    model = OCImportacion

class appointmentCreate(LoginRequiredMixin, CreateView):
    model = appointment
    form_class = AppointmentForm

    def get_initial(self):
      #patient = self.request.GET.get('patient')
      patient = "dsds"
      location = "Hola Q hace"
      producto= product(3,5)
      tomanomb = tomanombre()


      return {
        'Patient': patient,
        'Location': location,
        #'Duration':producto,
        'Clinician': tomanomb,
      }



class AboutView(TemplateView):
    template_name = 'about.html'

class SolCambDetailView(DetailView):
    model = SolCamb

class SolCambListView( ListView):

    model = SolCamb
    redirect_field_name = 'blog/post_list.html'

    def get_queryset(self):
        return SolCamb.objects.filter(published_date__isnull=True).order_by('-published_date')#sql query

'''
class SolCambListView(TemplateView):
    template_name = 'solcamb_list.html'

    model = SolCamb

    def get_queryset(self):
        return SolCamb.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')#sql query

    '''

class CreateSolCambView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirec_field_name = 'blog/solcamb_detail.html'

    form_class = SolCambForm

    model = SolCamb

    def get_initial(self):
          #patient = self.request.GET.get('patient')
          cliente = "Juanito"

          return {
            'cliente': cliente,
            }


class PostListView(ListView):
    model = Post


    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')#sql query

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirec_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirec_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


########################
########################

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)



@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def solcamb_publish(request, pk):
    solcamb = get_object_or_404(SolCamb, pk=pk)
    solcamb.publish()
    return redirect('solcamb_detail', pk=pk)



'''
@login_required
def editprofile(request):
    try:
    userprofile = UserProfiles.objects.get(user=request.user)
    except UserProfiles.DoesNotExist:
       return render(request, 'profile_edit.html', {'form':UserProfileForm()})
    form = UserProfileForm(instance=userprofile)
    return render(request, 'profile_edit.html', {'form':form})
'''

# Create your views here.
