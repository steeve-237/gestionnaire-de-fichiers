
from functions import *

system=platform.system()

def main(page:Page):
    page.title='filestransfert'
    page.bgcolor='black'
    page.window.height=700
    page.window.width=True

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

    poignee2.on_pan_update = resize2
    poignee2.height=sidebar.height
    workarea.on_hover = on_hover2
    poignee2.on_pan_update = resize2
    poignee2.height=sidebar.height
    workarea.on_hover = on_hover2
    backbutton.on_click=lambda e:loardchilditembackbutton()
    researchfield.on_change=lambda e,:onchangeresearch()
    researchicon.on_click=lambda e,:onchangeresearch()


    page.update()

    page.add(body)
    
    #print(page.window.width)
    loarddirhome(current_dir)
    page.update()
    page.on_resized=lambda e,p=page:updatepage(e,p)

app(target=main)