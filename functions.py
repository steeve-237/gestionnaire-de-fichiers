
from classes import *
current_dir=curent=Path().home().parent.parent

#####################################################################
#                                                                   #
#                        CREATION DES FONCTIONS                     #
#                                                                   #
#####################################################################

def resize2(e: DragUpdateEvent):
    global largeur_sidebar,pagewidth
    largeur_sidebar=sidebar.width

    #print(pagewidth, workarea.width)
    nouvelle_largeur = largeur_sidebar + e.delta_x
    if (249<nouvelle_largeur<(pagewidth//4)):
        largeur_sidebar=nouvelle_largeur
        sidebar.width = largeur_sidebar
        workarea.width = workarea.width - e.delta_x
        sidebar.update()
        workarea.update()
        titlesidebar.update()
        responsivezone.update()

poignee2.on_pan_update = resize2
poignee2.height=sidebar.height
#-----------------------------------------------------------------------------------------

def on_hover2(e: HoverEvent):
    if (poignee2.content.bgcolor==Colors.TRANSPARENT):
        poignee2.content.bgcolor=Colors.BLUE
    else:
        poignee2.content.bgcolor=Colors.TRANSPARENT

    poignee2.update()

workarea.on_hover = on_hover2

#-----------------------------------------------------------------------------------------

def updatepage(e,p):
    global pagewidth,pageheight

    pagewidth=p.width
    pageheight=p.height
    sidebar.width=p.width//4
    workarea.width=p.width//4*3
    sidebar.height=pageheight
    workarea.height=pageheight
    workareascrollable.height=pageheight-100
    sidebar.update()
    titlesidebar.update()
    workareascrollable.update()
    workarea.update()
#-----------------------------------------------------------------------------------------

poignee2.on_pan_update = resize2
poignee2.height=sidebar.height
workarea.on_hover = on_hover2

#-----------------------------------------------------------------------------------------
def loarddirhome(path:Path):
    global current_dir
    current_dir=path
    sidebar.content.controls=sidebar.content.controls[:1]

    list_dir=[]
    list_file=[]

    #on affiche d'abord les dossiers
    for element in current_dir.iterdir():
        if element.is_dir() and not element.name.startswith("."):
            list_dir.append(Item(name=element.name,father=current_dir,color=Colors.BLUE,type="dir"))
        elif element.is_file() and not element.name.startswith("."):
            list_file.append(Item(name=element.name,father=current_dir,color=Colors.BLUE,type="file"))

    list_dir=sorted(list_dir,key=lambda item:item.name)
    list_file=sorted(list_file,key=lambda item:item.name)

    for dir in list_dir:
        sidebar.content.controls.append(
            dir
        )
    for file in list_file:
        sidebar.content.controls.append(
            file
        )

#-----------------------------------------------------------------------------------------

backbutton.on_click=lambda e:loardchilditembackbutton()

#-----------------------------------------------------------------------------------------
def alert(*args):
    global list_item2
    

