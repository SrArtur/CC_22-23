# Configuración

En este documento se describe el proceso de la configuración de seguridad de git y Github siguiendo y atendiendo las indicaciones detalladas en [Hito 0: Descripción del problema a resolver usando correctamente git y GitHub](http://jj.github.io/CC/documentos/proyecto/0.Repositorio).



## Autenticación en dos pasos. 2FA

Para incrementar la seguridad de nuestra cuenta de Github 
podemos (es bastante recomendable) habilitar la autenticación en dos 
pasos o a partir de su traducción en inglés, segundo factor de 
autenticación.

Para ello es necesario ir al apartado *Settings* y a continuación, *Two-Factor authentication*.
 Tenemos la opción de hacerlo a través de un gestor de contraseñas o por
 el número de teléfono. Una vez terminado este proceso correctamente, ya tendríamos 
nuestra cuenta más segura. 

![](https://raw.githubusercontent.com/SrArtur/CC-22-23/main/docs/img/2FA.png)

## Edición del perfil

Es necesario modificar un perfil sobretodo si se ha creado nuevo. En el que es muy útil añadir datos como nuestro nombre completo, ciudad y universidad. Todo este proceso se puede hacer en el apartado *Edit Profile* en *Your profile*.

## Clave SSH

Siguiendo la [documentación de Github](https://docs.github.com/es/authentication/connecting-to-github-with-ssh) se pueden encontrar indicaciones y recomendaciones para llevar a cabo el proceso. Para ello, primero es crearnos un par de claves:

```
ssh-keygen -t rsa -b 4096 - C "aoa2eso@gmail.com"
Generating public/private rsa key pair.
Enter file in which to save the key (/c/Users/aoa2e/.ssh/id_rsa): id_portatil
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in id_portatil
Your public key has been saved in id_portatil.pub
The key fingerprint is:
SHA256:******************** aoa2eso@gmail.com
The key's randomart image is:
+---[RSA 4096]----+

+----[SHA256]-----+
```

Una vez tengamos el par de claves creados, el siguiente paso es añadir  el contenido de nuestra clave pública a Github. Lo podemos hacer en el apartado *SSH and GPG Keys* del apartado *Settings*.


