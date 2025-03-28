Dim SapGui, application, connection, session, WshShell, fso, folderPath
Dim valores, i
Dim anio, semestre, bimestre, sedeonline, usuario, contrasena
Dim fechaHoy

' 📌 Obtener la fecha actual en formato YYYY-MM-DD
fechaHoy = Year(Now) & "-" & Right("0" & Month(Now), 2) & "-" & Right("0" & Day(Now), 2)

' 📌 Ruta base donde se guardarán los archivos
basePath = "C:\Users\lgutierrez\OneDrive - Fundacion Instituto Profesional Duoc UC\SUDCRA\INDICE\"

' 📌 Crear la carpeta con la fecha de hoy
Set fso = CreateObject("Scripting.FileSystemObject")
folderPath = basePath & fechaHoy
If Not fso.FolderExists(folderPath) Then
    fso.CreateFolder folderPath
End If

' 📌 Definir valores manualmente
anio = "2025"
semestre = "1"
sedeonline = "80"
bimestre = "201"
usuario = "lgutierrez"
contrasena = "Fec4a5n5.007"

' 📌 Lista de valores para procesar
valores = Array(2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 18, 19, 29, 30, 74, 75, 76, 77, 79)

' 📌 Crear un objeto Shell para ejecutar SAP Logon
Set WshShell = CreateObject("WScript.Shell")

' 📌 Abrir SAP Logon
WshShell.Run """C:\Program Files (x86)\SAP\FrontEnd\SapGui\saplogon.exe"""
WScript.Sleep 5000 ' Esperar a que SAP Logon abra

' 📌 Conectar con SAP GUI Scripting
Set SapGui = GetObject("SAPGUI")
Set application = SapGui.GetScriptingEngine
Set connection = application.OpenConnection("Productivo", True) ' Seleccionar la conexión "pro"

' 📌 Obtener la sesión activa
Set session = connection.Children(0)

' 📌 Ingresar credenciales de usuario
session.findById("wnd[0]/usr/txtRSYST-MANDT").Text = "300" ' Mandante
session.findById("wnd[0]/usr/txtRSYST-BNAME").Text = usuario ' Usuario
session.findById("wnd[0]/usr/pwdRSYST-BCODE").Text = contrasena ' Contraseña
session.findById("wnd[0]/usr/txtRSYST-LANGU").Text = "ES" ' Idioma

' 📌 Presionar Enter para iniciar sesión
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/cntlIMAGE_CONTAINER/shellcont/shell/shellcont[0]/shell").doubleClickNode "F00002"

' 🔄 **Iniciar el ciclo para valores agrupados de 3 en 3**
For i = 0 To UBound(valores) Step 3
    ' Maximizar ventana
    session.findById("wnd[0]").maximize
    
    ' Ingresar Año y Semestre
    session.findById("wnd[0]/usr/ctxtANO").text = anio
    session.findById("wnd[0]/usr/ctxtSEMESTRE").text = semestre
    
    ' Ingresar los valores de la lista (agrupados de 3 en 3)
    session.findById("wnd[0]/usr/ctxtSEDE-LOW").text = valores(i)
    session.findById("wnd[0]/usr/btn%_SEDE_%_APP_%-VALU_PUSH").press
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").text = valores(i+1)
    session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,2]").text = valores(i+2)

    ' Ejecutar
    session.findById("wnd[1]/tbar[0]/btn[8]").press
    
    ' Guardar archivo Excel generado en la carpeta con la fecha de hoy
    session.findById("wnd[0]/usr/ctxtFILEMANE").text = folderPath & "\" & valores(i) & "_"
    session.findById("wnd[0]/tbar[1]/btn[8]").press
Next
' 🔄 **Finalizar Ciclo** 🔄

' 🔹 **Ejecutar proceso final con sede online**
session.findById("wnd[0]").maximize
session.findById("wnd[0]/usr/ctxtANO").text = anio
session.findById("wnd[0]/usr/ctxtSEMESTRE").text = bimestre
session.findById("wnd[0]/usr/ctxtSEDE-LOW").text = sedeonline

' 📌 Guardar archivo final en la carpeta con fecha
session.findById("wnd[0]/usr/ctxtFILEMANE").text = folderPath & "\" & sedeonline & "_"
session.findById("wnd[0]/tbar[1]/btn[8]").press

' 📌 Cerrar Excel automáticamente al finalizar
Call CerrarExcel

' 📌 Cerrar SAP automáticamente
Call CerrarSAP

' 📌 Liberar memoria y cerrar objetos
Set session = Nothing
Set connection = Nothing
Set application = Nothing
Set SapGui = Nothing
Set WshShell = Nothing
Set fso = Nothing

' 📌 Función para cerrar todos los procesos de Excel abiertos
Sub CerrarExcel()
    Dim objWMI, objProcess, objList
    Set objWMI = GetObject("winmgmts:\\.\root\cimv2").ExecQuery("SELECT * FROM Win32_Process WHERE Name='EXCEL.EXE'")
    
    For Each objProcess In objWMI
        objProcess.Terminate ' Cierra cada proceso de Excel abierto
    Next
    
    Set objWMI = Nothing
    Set objProcess = Nothing
End Sub

' 📌 Función para cerrar SAP automáticamente
Sub CerrarSAP()
    Dim objWMI, objProcess, objList
    Set objWMI = GetObject("winmgmts:\\.\root\cimv2").ExecQuery("SELECT * FROM Win32_Process WHERE Name='saplogon.exe' OR Name='sapgui.exe'")

    For Each objProcess In objWMI
        objProcess.Terminate ' Cierra cada proceso de SAP Logon y SAP GUI
    Next
    
    Set objWMI = Nothing
    Set objProcess = Nothing
End Sub
