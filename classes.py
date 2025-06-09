
from flet import *
from pathlib import *
import platform
import os
import subprocess
import time
from math import pi,fabs
from datetime import datetime,timedelta
import locale


#####################################################################
#                                                                   #
#                        CREATION DES VARIABLES                     #
#                                                                   #
#####################################################################

#donc height = true prend par defaut la hauteur egale a celle du parent

hauteur=True
largeur_sidebar = 250
largeur_workarea = 1000
pagewidth,pageheight=1000,1000
list_item2=[]
system=platform.system()
last_click_time=0
pages={}

current_dir=curent=Path().home().parent.parent #a la base le dossier courant cest la racine

# Conteneur 1 + poignée interne
poignee2 = GestureDetector(
    mouse_cursor=MouseCursor.RESIZE_LEFT_RIGHT,
    on_pan_update=None,  # on remplit plus tard
    content=Container(
        margin=margin.all(4),
        width=4,
        height=hauteur,
        bgcolor=Colors.TRANSPARENT,
        border_radius=4,
    ),
)

#poignee1.on_pan_update = resize1

backbutton=IconButton(
    icon=Icons.UNDO,
    icon_color=Colors.BLUE,
    icon_size=30,
    tooltip='back',
    rotate=20,
)

titlesidebar=Container(
    padding=padding.only(left=20,right=5),
    content=Text(
        value= "\U0001F4C1 {}".format(current_dir),
        color=Colors.GREEN_ACCENT_200,
        size=20,
        font_family="Times New Roman",
        text_align=TextAlign.START,
        max_lines=1,
    )
)

titlesidebarcontainer=Container(
    padding=padding.only(left=5),
    content=Row(
        controls=[
            backbutton,
            Row(
                width=350,
                scroll='auto',
                controls=[
                    titlesidebar,
                ]
            ),
        ]
    )
)

sendbutton=IconButton(
    icon=Icons.UPLOAD,
    icon_color=Colors.BLUE,
    icon_size=30,
    tooltip='envoyer',
)

researchicon=IconButton(
    icon=Icons.SEARCH,
    icon_size=30,
    icon_color=Colors.BLUE,
    tooltip="rechercher",
    on_click=lambda e:print("ok"),
)

researchfield=TextField(
    bgcolor=Colors.TRANSPARENT,
    color=Colors.BLUE,
    width=300,
    border_radius=20,
    border_color=Colors.TRANSPARENT,
    hint_text="rechercher",
    text_size=20,
    focus_color=Colors.BLUE,
    label_style=TextStyle(color=Colors.BLUE,font_family="Courier New",size=20),
    hint_style=TextStyle(color=Colors.BLUE,font_family="Courier New",size=20),
)

researchzone=Container(
    padding=padding.only(left=2,right=2),
    margin=margin.only(bottom=5,right=15,top=5),
    border_radius=30,
    border=border.all(1,Colors.BLUE),
    bgcolor=Colors.TRANSPARENT,
    content=Row(
        controls=[
            researchicon,
            researchfield,
        ]
    )
)
optionbar=Container(
    bgcolor=Colors.TRANSPARENT,
    margin=margin.only(left=2,right=20),
    height=60,
    border_radius=50,
    border=border.only(bottom=BorderSide(2,Colors.BLUE)),
    alignment=alignment.center,
    content=Row(
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=VerticalAlignment.CENTER,
        controls=[
            titlesidebarcontainer,
            sendbutton,
            researchzone,
        ]
    )
)

responsivezone=ResponsiveRow(
    spacing=0,
    run_spacing=0,
    controls=[
        
    ]
)

workareascrollable=Container(
    margin=margin.only(left=2,right=30),
    height=pageheight-100,
    content=Column(
        scroll='auto',
        alignment=alignment.center,
        controls=[
            responsivezone,
        ]
    )
    
)

workarea=Container(
    border=border.all(1,Colors.WHITE),
    height=True,
    width=1000,
    border_radius=25,
    expand_loose=True,
    content=Row(
        controls=[
            poignee2,
            Container(
                bgcolor=Colors.TRANSPARENT,
                margin=margin.only(left=2,right=2),
                height=True,
                expand=True,
                content=Column(
                    spacing=2,
                    controls=[
                        optionbar,
                        workareascrollable,
                    ]
                )
            )
        ]
    )
)



sidebar=Container(
    height=pageheight,
    border_radius=25,
    border=border.all(1,Colors.WHITE),
    bgcolor=Colors.TRANSPARENT,
    width=250,
    content=Column(
        scroll='auto',
        spacing=2,
        expand=True,
        expand_loose=True,
        alignment=MainAxisAlignment.START,
        horizontal_alignment=CrossAxisAlignment.START,
        controls=[
        ]
    )
)

accueil=Container(
    expand=True,
    border_radius=25,
    bgcolor=Colors.GREY_900,
    content=Row(
        spacing=5,
        controls=[
            sidebar,
            workarea,
        ]
    ),
)

pages={
    "/accueil":View(
        route="/",
        bgcolor=Colors.BLACK,
        controls=[
            accueil,
        ],
    ),
}


class Item2(Container):
    def openfile(self,*args):
        if self.type!="dir":
            if system=="Windows":
                os.startfile(self.father/self.name)
            elif system=="Darwin": #pour macOs 
                subprocess.run(["open",self.father/self.name])
            elif system=="Linux":
                try:
                    subprocess.run(["xdg-open",self.father/self.name])
                except Exception as e:
                    print("erreur!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",e)

    def loardchilditems2(self,e,*args):
        global current_dir,list_item2,last_click_time
        curent_lick_time=time.time()
        if curent_lick_time - last_click_time > 0.5:

            list_dir2=[]
            list_file2=[]

            if self.type=="dir": #sil est un dossier
                current_dir=self.father/self.name
                str_curent_dir=str(current_dir)

                titlesidebar.content.value="\U0001F4C1 "+ str_curent_dir
                titlesidebar.update()

                for element in current_dir.iterdir(): #on les gardent d'abord dans deux listes afin de les trier par ordre alphabetique
                    if element.is_dir() and not element.name.startswith("."):
                        list_dir2.append(Item2(name=element.name,father=current_dir,color=Colors.BLUE,type="dir"))
                    elif element.is_file() and not element.name.startswith("."):
                        list_file2.append(Item2(name=element.name,father=current_dir,color=Colors.BLUE,type="file"))

                #on fati le trie sur le nom du item

                list_dir2=sorted(list_dir2,key=lambda item:item.name)
                list_file2=sorted(list_file2,key=lambda item:item.name)
                list_item2=list_dir2+list_file2

                responsivezone.controls=[
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
        else:
            self.openfile()

        last_click_time=curent_lick_time
        responsivezone.update()

    def __init__(self,name:str,father:Path,type:str,color:Colors,family="Courier New",**kwargs):
        super().__init__(**kwargs)
        self.name=name
        self.father=father
        self.type=type
        self.color=color
        self.tooltip=Tooltip(
            message=self.name[:20]+"..."+self.name[-8:],
            bgcolor=Colors.TRANSPARENT,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(color=Colors.BLUE),
        )
        if len(self.name)<29:
            self.tooltip.message=self.name

        self.title=Text(
            value=self.name,
            size=12,
            color=Colors.BLUE,
            max_lines=1,
            width=50,
            text_align=TextAlign.CENTER,
        )

        if (self.type=="dir"):
            self.mainicon=Icon(name=Icons.FOLDER,color=Colors.AMBER,size=30)
        else:
            ext = Path(name).suffix.lower()
            iconname=Icons.INSERT_DRIVE_FILE
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                iconname=Icons.IMAGE
            elif ext in ['.mp3', '.wav', '.ogg']:
                iconname=Icons.AUDIOTRACK
            elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
                iconname=Icons.MOVIE
            elif ext == '.pdf':
                iconname=Icons.PICTURE_AS_PDF
            elif ext in ['.doc', '.docx']:
                iconname=Icons.TEXT_SNIPPET
            elif ext in ['.xls', '.xlsx', '.csv']:
                iconname=Icons.TABLE_CHART
            elif ext in ['.zip', '.rar', '.tar', '.gz']:
                iconname=Icons.ARCHIVE
            elif ext in ['.py', '.js', '.cpp', '.java', '.html','.c','.sql','.php','.css']:
                iconname=Icons.CODE

            self.mainicon=Icon(name=iconname,color=Colors.GREEN,size=25)

        self.content=IconButton(
            on_click=lambda e, objet=self:self.loardchilditems2(e,objet),
            content=Column(
                spacing=2,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                alignment=alignment.center,
                controls=[
                    self.mainicon,
                    self.title,
                ]
            ),
        )

class Item(Container):#les filtres sur les types de cycle de la side nave
    
    def openfile(self,*args):
        if self.type!="dir":
            if system=="Windows":
                os.startfile(self.father/self.name)
            elif system=="Darwin": #pour macOs 
                subprocess.run(["open",self.father/self.name])
            elif system=="Linux":
                try:
                    subprocess.run(["xdg-open",self.father/self.name])
                except Exception as e:
                    print("erreur!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",e)

    def loardchilditems(self,e,*args):
        global current_dir,list_item2,last_click_time
        curent_lick_time=time.time()
        if curent_lick_time - last_click_time > 0.5:
            list_dir=[]
            list_file=[]
            list_dir2=[]
            list_file2=[]

            if self.type=="dir": #sil est un dossier
                if self.foled=="yes": #s'il n'est pas encore deployé on le deploye
                    current_dir=self.father/self.name
                    str_curent_dir=str(current_dir)

                    titlesidebar.content.value="\U0001F4C1 "+ str_curent_dir
                    titlesidebar.update()
                    self.foledicon.name=Icons.KEYBOARD_ARROW_DOWN

                    if len(self.content.content.content.controls)==1:#s'il na qu'un seul fils (son titre) ca veut dire qu'on ne l'a jamais ouvert
                        for element in current_dir.iterdir(): #on les gardent d'abord dans deux listes afin de les trier par ordre alphabetique
                            if element.is_dir() and not element.name.startswith("."):
                                list_dir.append(Item(name=element.name,father=current_dir,color=Colors.BLUE,type="dir"))
                                list_dir2.append(Item2(name=element.name,father=current_dir,color=Colors.BLUE,type="dir"))
                            elif element.is_file() and not element.name.startswith("."):
                                list_file.append(Item(name=element.name,father=current_dir,color=Colors.BLUE,type="file"))
                                list_file2.append(Item2(name=element.name,father=current_dir,color=Colors.BLUE,type="file"))

                        #on fati le trie sur le nom du item
                        list_dir=sorted(list_dir,key=lambda item:item.name)
                        list_file=sorted(list_file,key=lambda item:item.name)

                        list_dir2=sorted(list_dir2,key=lambda item:item.name)
                        list_file2=sorted(list_file2,key=lambda item:item.name)
                        list_item2=list_dir2+list_file2

                        responsivezone.controls=[
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

                        #on insert l'item
                        for dir in list_dir:
                            self.content.content.content.controls.append(
                                dir
                            )

                        for file in list_file:
                            self.content.content.content.controls.append(
                                file
                            )

                    else: #sinon il avait deja ete ouvert auparavant donc on rerend visible tous ses enfants  
                        for elt in self.content.content.content.controls[1:]:
                            elt.visible=True

                    self.foled="no" #on le met a l'etat deployé
                    
                else: #s'il est deja deployé on le referme
                    str_curent_dir=str(current_dir)
                    titlesidebar.content.value="\U0001F4C1 "+ str_curent_dir
                    titlesidebar.update()
                    self.foledicon.name=Icons.CHEVRON_RIGHT


                    self.content.content.content.controls=self.content.content.content.controls[:1]

                    #(self.father/self.name).resolve().relative_to(current_dir.resolve()) # si oui alors le dossier courant est un sous dossier du dossier actuel on ne peut pas le detruire


                    self.foled="yes"
        else:
            self.openfile()

        last_click_time=curent_lick_time
        self.update()
        responsivezone.update()


    def __init__(self,name:str,father:Path,type:str,color:Colors,foled="yes",family="Courier New",**kwargs):
        super().__init__(**kwargs)
        self.name=name
        self.father=father
        self.type=type
        self.foled=foled
        self.color=color
        self.title=Text(self.name,size=15,color=Colors.BLUE)
        #self.on_click=lambda e, objet=self:self.loardchilditems(e,objet)

        if (self.type=="dir"):
            self.mainicon=Icon(name=Icons.FOLDER,color=Colors.AMBER,size=30)
            self.margin=margin.only(left=0)
            if(self.foled=='yes'):
                self.foledicon=Icon(name=Icons.KEYBOARD_ARROW_RIGHT,color=Colors.BLUE,size=20)
        else:
            self.margin=margin.only(left=20)
            ext = Path(name).suffix.lower()
            iconname=Icons.INSERT_DRIVE_FILE
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                iconname=Icons.IMAGE
            elif ext in ['.mp3', '.wav', '.ogg']:
                iconname=Icons.AUDIOTRACK
            elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
                iconname=Icons.MOVIE
            elif ext == '.pdf':
                iconname=Icons.PICTURE_AS_PDF
            elif ext in ['.doc', '.docx']:
                iconname=Icons.TEXT_SNIPPET
            elif ext in ['.xls', '.xlsx', '.csv']:
                iconname=Icons.TABLE_CHART
            elif ext in ['.zip', '.rar', '.tar', '.gz']:
                iconname=Icons.ARCHIVE
            elif ext in ['.py', '.js', '.cpp', '.java', '.html']:
                iconname=Icons.CODE

            self.mainicon=Icon(name=iconname,color=Colors.GREEN,size=25)
            self.foledicon=Container(content=None)

        self.frametitle=IconButton(
            content=Row(
                controls=[
                    self.foledicon,
                    self.mainicon,
                    self.title,
                ]
            ),
        )

        self.frametitle.on_click=lambda e, objet=self:self.loardchilditems(e,objet)

        self.content=Container(
            bgcolor=Colors.TRANSPARENT,
            margin=margin.only(left=10),
            content=Container(
                margin=margin.only(left=0),
                content=Column(
                    controls=[
                        self.frametitle,
                    ]
                )
            )
        )

#-----------------------------------------------------------------------------------------
