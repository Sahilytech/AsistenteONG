"""Sistema visual único para toda la aplicación. Los colores son adaptativos."""
COLORS={
 "background":("#F7FAFC","#101417"),"surface":("#FFFFFF","#171D21"),"surface_alt":("#F1F6F9","#1D262B"),"surface_blue":("#EAF7FC","#172B33"),
 "primary":("#0e98d6","#36B7ED"),"primary_dark":("#0879ad","#1689BA"),"primary_soft":("#DFF3FB","#173D4D"),"primary_pale":("#F5FBFE","#14242B"),
 "text":("#111111","#F4F7F8"),"text_muted":("#65727B","#AAB8BF"),"text_soft":("#89949B","#7F9098"),"border":("#D9E5EA","#2B383F"),"border_strong":("#C4D6DE","#3A4B54"),
 "success":("#168A4A","#49C58A"),"success_soft":("#E9F7EF","#173A2B"),"warning":("#B86A00","#F0B35A"),"warning_soft":("#FFF4E5","#3D2E19"),"danger":("#C62828","#FF7373"),"danger_soft":("#FDECEC","#432020")}
FONTS={"display":("Helvetica",28,"bold"),"title":("Helvetica",21,"bold"),"heading":("Helvetica",15,"bold"),"subheading":("Helvetica",12,"bold"),"body":("Helvetica",11),"body_bold":("Helvetica",11,"bold"),"small":("Helvetica",9),"small_bold":("Helvetica",9,"bold"),"tiny":("Helvetica",8)}
SPACING={"xs":5,"sm":9,"md":14,"lg":20,"xl":28,"xxl":36}; CARD_RADIUS=16; BUTTON_HEIGHT=38

def switch_theme(theme:str):
    """Mantiene compatibilidad: CustomTkinter resuelve los pares claro/oscuro."""
    return COLORS
