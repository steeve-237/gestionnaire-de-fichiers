
from functions import *

system=classes.platform.system()


def main(page:Page):
    def changeroute(*agrs):
        page.views.clear()
        page.views.append(
            classes.pages[page.route]
        )
        page.update()

    page.title='filestransfert'
    page.bgcolor='black'
    page.window.height=700
    page.window.width=True

    page.on_resized=lambda e,p=page:updatepage(e,p)
    page.on_route_change=changeroute

    page.theme=Theme(
        scrollbar_theme=ScrollbarTheme(
            track_color={
                ControlState.HOVERED: Colors.WHITE, #je ne sais pas a quoi ca sert
                ControlState.DEFAULT: Colors.TRANSPARENT, #je ne sais pas a quoi ca sert
            },
            track_visibility=True,
            thumb_visibility=True,
            thumb_color={
                ControlState.HOVERED: Colors.BLUE,
                ControlState.DEFAULT: Colors.BLUE,
            },
            thickness=5,
            track_border_color=Colors.BLUE,
            radius=10,
            main_axis_margin=5,
            cross_axis_margin=1,
        ),
    )

    classes.poignee2.on_pan_update = resize2
    classes.poignee2.height=classes.sidebar.height
    classes.workarea.on_hover = on_hover2
    classes.poignee2.on_pan_update = resize2
    classes.poignee2.height=classes.sidebar.height
    classes.workarea.on_hover = on_hover2
    classes.backbutton.on_click=lambda e:loardchilditembackbutton()
    classes.researchfield.on_change=lambda e,:onchangeresearch()
    classes.researchicon.on_click=lambda e,:onchangeresearch()

    #page.add(classes.body)
    
    page.go("/accueil")
    loarddirhome(classes.current_dir)
    page.update()


app(target=main)