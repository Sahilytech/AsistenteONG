"""Sistema visual de Asistente ONG: claro, oscuro y adaptado al sistema."""
LIGHT={"background":"#F7FAFC","surface":"#FFFFFF","surface_alt":"#F1F6F9","surface_blue":"#EAF7FC","primary":"#0e98d6","primary_dark":"#0879ad","primary_soft":"#DFF3FB","primary_pale":"#F5FBFE","text":"#111111","text_muted":"#65727B","text_soft":"#89949B","border":"#D9E5EA","border_strong":"#C4D6DE","success":"#168A4A","success_soft":"#E9F7EF","warning":"#B86A00","warning_soft":"#FFF4E5","danger":"#C62828","danger_soft":"#FDECEC"}
DARK={"background":"#101417","surface":"#171D21","surface_alt":"#1D262B","surface_blue":"#172B33","primary":"#36B7ED","primary_dark":"#1689BA","primary_soft":"#173D4D","primary_pale":"#14242B","text":"#F4F7F8","text_muted":"#AAB8BF","text_soft":"#7F9098","border":"#2B383F","border_strong":"#3A4B54","success":"#49C58A","success_soft":"#173A2B","warning":"#F0B35A","warning_soft":"#3D2E19","danger":"#FF7373","danger_soft":"#432020"}
COLORS=dict(LIGHT)
FONTS={"display":("Helvetica",28,"bold"),"title":("Helvetica",21,"bold"),"heading":("Helvetica",15,"bold"),"subheading":("Helvetica",12,"bold"),"body":("Helvetica",11),"body_bold":("Helvetica",11,"bold"),"small":("Helvetica",9),"small_bold":("Helvetica",9,"bold"),"tiny":("Helvetica",8)}
SPACING={"xs":5,"sm":9,"md":14,"lg":20,"xl":28,"xxl":36}; CARD_RADIUS=16; BUTTON_HEIGHT=38

def switch_theme(theme:str):
    global COLORS
    COLORS=dict(DARK if theme == "dark" else LIGHT)
    return COLORS
