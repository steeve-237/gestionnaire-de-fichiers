from flet import *
import classes

current_dir=classes.Path().home().parent.parent

#####################################################################
#                                                                   #
#                        CREATION DES FONCTIONS                     #
#                                                                   #
#####################################################################

def resize2(e: DragUpdateEvent):
    global largeur_sidebar,pagewidth
    largeur_sidebar=classes.sidebar.width

    #print(pagewidth, workarea.width)
    nouvelle_largeur = largeur_sidebar + e.delta_x
    if (249<nouvelle_largeur<(pagewidth//4)):
        largeur_sidebar=nouvelle_largeur
        classes.sidebar.width = largeur_sidebar
        classes.workarea.width = classes.workarea.width - e.delta_x
        classes.sidebar.update()
        classes.workarea.update()
        classes.titlesidebar.update()
        classes.responsivezone.update()

classes.poignee2.on_pan_update = resize2
classes.poignee2.height=classes.sidebar.height
#-----------------------------------------------------------------------------------------

def on_hover2(e: HoverEvent):
    if (classes.poignee2.content.bgcolor==Colors.TRANSPARENT):
        classes.poignee2.content.bgcolor=Colors.BLUE
    else:
        classes.poignee2.content.bgcolor=Colors.TRANSPARENT

    classes.poignee2.update()

classes.workarea.on_hover = on_hover2

#-----------------------------------------------------------------------------------------

def updatepage(e,p):
    global pagewidth,pageheight

    pagewidth=p.width
    pageheight=p.height
    classes.sidebar.width=p.width//4
    classes.workarea.width=p.width//4*3
    classes.sidebar.height=pageheight
    classes.workarea.height=pageheight
    classes.workareascrollable.height=pageheight-100
    classes.sidebar.update()
    classes.titlesidebar.update()
    classes.workareascrollable.update()
    classes.workarea.update()
#-----------------------------------------------------------------------------------------

classes.poignee2.on_pan_update = resize2
classes.poignee2.height=classes.sidebar.height
classes.workarea.on_hover = on_hover2

#-----------------------------------------------------------------------------------------
def loarddirhome(path:classes.Path):
    global current_dir
    current_dir=path
    classes.sidebar.content.controls=classes.sidebar.content.controls[:1]

    list_dir=[]
    list_file=[]

    #on affiche d'abord les dossiers
    for element in current_dir.iterdir():
        if element.is_dir() and not element.name.startswith("."):
            list_dir.append(classes.Item(name=element.name,father=current_dir,color=Colors.BLUE,type="dir"))
        elif element.is_file() and not element.name.startswith("."):
            list_file.append(classes.Item(name=element.name,father=current_dir,color=Colors.BLUE,type="file"))

    list_dir=sorted(list_dir,key=lambda item:item.name)
    list_file=sorted(list_file,key=lambda item:item.name)

    for dir in list_dir:
        classes.sidebar.content.controls.append(
            dir
        )
    for file in list_file:
        classes.sidebar.content.controls.append(
            file
        )

#-----------------------------------------------------------------------------------------

classes.backbutton.on_click=lambda e:classes.loardchilditembackbutton()

#-----------------------------------------------------------------------------------------
def loardchilditembackbutton(*args):
    global list_item2
 
    list_dir2=[]
    list_file2=[]
    
    classes.current_dir=classes.current_dir.parent
    str_curent_dir=str(classes.current_dir)

    classes.titlesidebar.content.value="\U0001F4C1 "+ str_curent_dir
    classes.titlesidebar.update()

    for element in classes.current_dir.iterdir(): #on les gardent d'abord dans deux listes afin de les trier par ordre alphabetique
        if element.is_dir() and not element.name.startswith("."):
            list_dir2.append(classes.Item2(name=element.name,father=classes.current_dir,color=Colors.BLUE,type="dir"))
        elif element.is_file() and not element.name.startswith("."):
            list_file2.append(classes.Item2(name=element.name,father=classes.current_dir,color=Colors.BLUE,type="file"))

    #on fati le trie sur le nom du item

    list_dir2=sorted(list_dir2,key=lambda item:item.name)
    list_file2=sorted(list_file2,key=lambda item:item.name)
    list_item2=list_dir2+list_file2

    classes.responsivezone.controls=[
        Container(
            col={"sm": 12/5, "md": 12/10, "xl": 12/15},
            padding=padding.all(5),
            content=Column(
                spacing=2,
                controls=[
                item2,
                ]
            )
        ) for item2 in list_item2
    ]

    classes.responsivezone.update()

classes.backbutton.on_click=lambda e:loardchilditembackbutton()

#-----------------------------------------------------------------------------------------

def onchangeresearch(*args):
    research_list_item2=[]
    for item in classes.list_item2:
        if (classes.researchfield.value.lower() in item.name.lower()):
            research_list_item2.append(item)

    classes.responsivezone.controls=[
        Container(
            col={"sm": 12/5, "md": 12/10, "xl": 12/15},
            padding=padding.all(5),
            content=Column(
                spacing=2,
                controls=[
                item2,
                ]
            )
        ) for item2 in research_list_item2
    ]
        
    classes.responsivezone.update()

classes.researchfield.on_change=lambda e,:onchangeresearch
classes.researchicon.on_click=lambda e,:onchangeresearch

#-----------------------------------------------------------------------------------------
