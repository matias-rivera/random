
# coding: utf-8

# ### Backoff Algorithm

# Cuando k terminales tratan de enviar paquetes de datos en una misma red, si estos son enviados al mismo tiempo ocurre una colisión. Cuando las terminales no reciben una respuesta vuelven a enviar un mensaje pero con un retraso(delay) para evitar una posible colisión. El delay tomará valores entre:

# <img src="backoff1.jpg">

# Siendo 'n' el número de intentos.
# Si vuelve a colisionar, n incrementa en 1.

# In[29]:


from random import randint


# In[30]:


class Node:
    Counter = 0
    def __init__(self):
        Node.Counter += 1
        self.name = "PC" + str(Node.Counter)
        self.delay = randint(0, 1)
        self.attempt = 0
        self.occurrence = self.delay
   
    def backoff(self):
        self.attempt+=1
        aux = (2 ** self.attempt) -1
        self.delay = randint(0, aux)
        self.occurrence += 1 + self.delay
        
    def reset(self):
        self.delay = randint(0, 1)
        self.attempt = 0
        self.occurrence += 1 + self.delay
    
    def printNode(self):
        print("%s(%d)(%d)"%(self.name,self.delay,self.occurrence))
        
    
    def displayNow(self,time):
        print('%s (%d)' % (self.name,self.delay),end="")
        
        if self.occurrence == time:
            print('\033[94m' +"("+str(self.occurrence)+")"+'\033[0m')
        else:
            print("(%d)"%(self.occurrence))
        


# #### Funciones para cambiar el color

# In[31]:


def green(s):
    print('\033[92m' + s + '\033[0m', end="")

def blue(s):
    print('\033[94m' + s + '\033[0m',end="")

def red(s):
    print('\033[91m' + s + '\033[0m',end="")


# #### Imprime la lista de los retrasos y ocurrencias en el siguiente formato:
# Nombre de Equipo(Retraso)(Ocurrencia)

# In[32]:


def printList(listN,time):
    for i in listN:
        i.displayNow(time)



# #### En este programa se tomará en cuenta el tiempo, si los nodos envían mensajes al mismo tiempo ocurrirá una colisión. 

# In[37]:


Node.Counter = 0

#tiempo
time = 20
#contador de colisiones
counter = 0
#n° de nodos
nodes = 4
#lista de nodos
listN = []
#lista de colisiones
listC = []

#llena la lista con el n° de nodos
for x in range(0,nodes):
        listN.append(Node())
        
for time in range(0,time+1):
    print("__________________________________")
    print("")
    print("time:", end="")
    blue(str(time)+"s")
    print("")
    
    #Imprime la lista de los actuales retrasos y ocurrencias.
    printList(listN,time)
    
    
    for i in listN:
    
        for j in listN:
            
            #Si ocurre una colision
            if i.occurrence == j.occurrence and i.name != j.name and i.occurrence == time and i.name not in listC:
                
                #Se agrega a la lista de colisiones
                listC.append(i.name)
                counter += 1
    
    #Si ha ocurrido una colisión en la iteración la lista no estará vacía
    print("--------------")
    if listC:
        
        red("Collision")
        print("")
        print(listC)
    else:
        green("No Collision")
        print("")
    print("--------------")
    
    #Verifica la ocurrencia con el tiempo
    for i in listN:
        
        #Si el elemento colisiona se procede a aplica el método backoff
        if i.name in listC:
            i.backoff()
            red(">backoff: ")
            i.printNode()
 
            
        #Si el elemento no colisiona se resetea el retraso(delay) y vuelve a enviar otro paquete
        if i.name not in listC and i.occurrence == time:
            i.reset()
            green(">reset: ")
            i.printNode()
    
    #Se reinicia la lista de colisiones para la siguiente iteración
    listC = []

