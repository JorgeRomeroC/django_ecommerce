from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

    # FUNCION QUE NOS PERMITIRA CREAR UN NUEVO USUARIO Y TAMBIEN UN SUPERUSUARIO

class MyAccountManager(BaseUserManager):

    # ===========================================
    # ESTA FUNCION NOS PERMITE CREAR UN USUARIO
    # ===========================================

    def create_user(self, first_name, last_name, username, email, password=None):
        #SI NO ESTOY PASANDO UN EMAIL O EL VALOR DEL EMAIL ES NULO, ARROJE UN ERROR
        if not email:
            raise ValueError('El usuario debe tener un email')
        if not username:
            raise ValueError('El usuario debe tener un username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #===========================================
    # ESTA FUNCION NOS PERMITE CREAR UN SUPER USUARIO
    #===========================================
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        # SETEAR ALGUNOS ATRIBUTOS O VALORES QUE DEBE TENER UN ADMINISTRADOR
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

#===========================================
# CREANDO MODELO Y CAMPOS QUE NOS PERMITA
# SABER LA ACTIVIDAD DEL USUARIO EN EL SISTEMA
# Y SU NIVEL DE ACCESO
#===========================================
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # Campos atributos django
    #FECHA EN LA QUE FUE CREADO EL USUARIO
    date_joined = models.DateTimeField(auto_now_add=True)
    #FECHA EN QUE EL USUARIO HIZO LOGIN POR ULTIMA VEZ
    last_login = models.DateTimeField(auto_now_add=True)
    # ¿ EL USUARIO ES ADMINISTRADOR?
    is_admin = models.BooleanField(default=False)
    # ¿ ES PARTE DEL STAF
    is_staff = models.BooleanField(default=False)
    # ¿ EL USUARIO ESTA ACTIVO ?
    is_active = models.BooleanField(default=False)
    # ¿ EL USUARIO ES SUPER ADMIN ?
    is_superadmin = models.BooleanField(default=False)


    # SOLICITAMOS QUE EL USUARIO INGRESE EL EMAIL y NO EL USERNAME
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    # INTEGRAMOS LAS FUNCIONES PARA CREAR UN USUARIO Y LE SUPER USUARIO
    objects = MyAccountManager()

    # el campo que represente a cada usuario sera el EMAIL
    def __str__(self):
        return self.email

    # SOLO SI ES ADMIN, TENDRA LOS PERMISOS PARA HACER MODIFICACIONES
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # SI ES ADMIN , DEBO INDICAR QUE TAMBIEN TENGA ACCESO A LOS MODULOS
    def has_module_perms(self, add_label):
        return True