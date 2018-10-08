from django import forms
from django.forms import formset_factory, modelformset_factory
from blog.models import Post,Comment,SolCamb, appointment, OCImportacion, ProdID, Book, Author, PruebaMod, ProdReal


class PruebaModForm(forms.ModelForm):
    class Meta:
        model = PruebaMod
        fields = ['dato1', 'dato2', 'ultrafile']



class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', )
        labels = {
            'name': 'Book Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Book Name here'
                }
            )
        }

AuthorFormset = modelformset_factory(
    Author,
    fields=('name', ),
    extra=1,
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Author Name here'
            }
        )
    }
)

#Para el ejemplo de dynamic form creation
class BookForm(forms.Form):
    name = forms.CharField(
        label='Book Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    )
BookFormset = formset_factory(BookForm, extra=1)

BookModelFormset = modelformset_factory(
    Book,
    fields=('name', ),
    extra=1,
    widgets={'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    }
    )


class OCImportacionForm(forms.ModelForm):
    class Meta:
        model = OCImportacion
        fields = ['oc', 'proveedor', 'mes_arribo_esperado', 'create_date',]


class AppointmentForm(forms.ModelForm):

    distance = forms.CharField(max_length=20, required = False)
    class Meta:
        model = appointment

        fields = ['Patient', 'Date', 'Time', 'Duration', 'Location',   'Clinician', 'AppointmentType']

class ProdIDForm(forms.ModelForm):
    class Meta:
        model = ProdID
        fields = ['duracion', 'workcenter']



class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')



class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text')
        widget = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})#se conecta el atribut texto con tres clases, una mía y otras dos de CSS

        }



class CommentForm(forms.ModelForm):
    class Meta():
        model=Comment
        fields = ('author','text')
        widget = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }

class SolCambForm(forms.ModelForm):

    motivo = forms.CharField(label='motivo', max_length=100)

    class Meta():
        model=SolCamb
        fields = ('title','author','text', 'id', 'cliente')
        widget = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
            'id':forms.Textarea(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'textinputclass'}),
        }
