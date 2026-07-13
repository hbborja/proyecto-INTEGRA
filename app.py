from flask import Flask, render_template, request, redirect, url_for
from conexion import get_db_connection

app = Flask(__name__)
app.secret_key = 'mi_llave_secreta_super_segura' # <-- AGREGA ESTA LÍNEA



# =========================================================
# 1. MOSTRAR CUENTAS (Tu vista principal con la tabla)
# =========================================================
@app.route("/cuenta")
def mostrar_cuentas():
    # Leemos si la URL tiene el '?exito=true'
    registro_exitoso = request.args.get('exito') == 'true'
    registro_eliminado = request.args.get('eliminado') == 'true'
    registro_actualizado = request.args.get('actualizado') == 'true'
    
    conn = get_db_connection()
    cuentas = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo_cuenta, nombre_cuenta, tipo_cuenta_padre FROM cuentas_contables ORDER BY codigo_cuenta")
            cuentas = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Error al listar cuentas: {e}")
        finally:
            conn.close()
            
        # PASAMOS LA VARIABLE 'registro_exitoso' a tu HTML
        return render_template("modules/contabilidad/cuenta.html", cuentas=cuentas, registro_exitoso=registro_exitoso, registro_eliminado=registro_eliminado,registro_actualizado=registro_actualizado)
    return "Error al conectar a la base de datos"


# =========================================================
# 2. INSERTAR CUENTA (El formulario que procesa el INSERT)
# =========================================================
@app.route("/insertar", methods=["POST"])
def insertar_cuenta():
    if request.method == "POST":
        codigo_cuenta = request.form["codigo_cuenta"]
        nombre_cuenta = request.form["nombre_cuenta"]
        tipo_cuenta_padre = request.form["tipo_cuenta_padre"]

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO cuentas_contables (codigo_cuenta, nombre_cuenta, tipo_cuenta_padre) VALUES (:codigo, :nombre, :tipo)",
                    codigo=codigo_cuenta, nombre=nombre_cuenta, tipo=tipo_cuenta_padre
                )
                conn.commit()
                cursor.close()
                flash('registro_exitoso') # Activador para tu modal flotante de éxito si lo usas
            except Exception as e:
                print(f"Error al insertar en Oracle: {e}")
            finally:
                conn.close()
            
            # CORREGIDO: Redirige al nombre de la función 'mostrar_cuentas'
            return redirect(url_for("mostrar_cuentas", exito="true"))
            
        return "Error al conectar a la base de datos"


# =========================================================
# 3. ACTUALIZAR CUENTA (El modal envía los datos aquí mediante POST)
# =========================================================
@app.route('/actualizar', methods=['POST'])
def actualizar():
    if request.method == 'POST':
        codigo = request.form['codigo_cuenta']
        nombre = request.form['nombre_cuenta']
        tipo = request.form['tipo_cuenta_padre']
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = """UPDATE cuentas_contables 
                         SET nombre_cuenta = :1, tipo_cuenta_padre = :2 
                         WHERE codigo_cuenta = :3"""
                cursor.execute(sql, (nombre, tipo, codigo))
                conn.commit()
                cursor.close()
            except Exception as e:
                print(f"Error al actualizar la cuenta: {e}")
            finally:
                conn.close()
                
        # CORREGIDO: Redirige a 'mostrar_cuentas'
        return redirect(url_for('mostrar_cuentas',actualizado="true"))


# =========================================================
# 4. ELIMINAR CUENTA (El modal de borrado envía el código aquí)
# =========================================================
@app.route("/eliminar", methods=["POST"])
def eliminar_cuenta():
    if request.method == 'POST':
        codigo_cuenta = request.form.get('codigo_cuenta') 
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cuentas_contables WHERE codigo_cuenta = :codigo", codigo=codigo_cuenta)
                conn.commit()
                cursor.close()
            except Exception as e:
                print(f"Error al eliminar en Oracle: {e}")
            finally:
                conn.close()
                
            # CORREGIDO: Redirige a 'mostrar_cuentas'
            return redirect(url_for("mostrar_cuentas", eliminado="true")) 
            
        return "Error al conectar a la base de datos"

@app.route("/")
def  loguin():
    return render_template("index.html") # El nombre de tu HTML principal


@app.route("/nomina")
def pagina_nomina():
    # Si tus otras páginas de nómina sí están en subcarpetas, aquí sí especificas la ruta:
    return render_template("modules/nomina/index.html") # (O el nombre de tu archivo i

@app.route("/contabilidad") # <-- La URL que se verá en el navegador
def pagina_contabilidad():  # <-- ¡ESTE NOMBRE debe ser idéntico al del HTML!
    
    # Aquí pones la ruta real de tu HTML de contabilidad
    return render_template("modules/contabilidad/index.html")

@app.route("/mantenimiento") # <-- La URL que se verá en el navegador
def pagina_mantenimiento():  # <-- ¡ESTE NOMBRE debe ser idéntico al del HTML!
    
    # Aquí pones la ruta real de tu HTML de mantenimiento
    return render_template("modules/mantenimiento/index.html")

@app.route("/biblioteca") # <-- La URL que se verá en el navegador
def pagina_biblioteca():  # <-- ¡ESTE NOMBRE debe ser idéntico al del HTML!
    
    # Aquí pones la ruta real de tu HTML de biblioteca
    return render_template("modules/biblioteca/index.html")

# para nomina ul
# 2. Opción: Motivos Ingreso/Egreso
@app.route("/nomina/motivos")
def pagina_motivos():  
    return render_template("modules/nomina/motivos.html") 

# 3. Opción: Gestión de Nómina
@app.route("/nomina/gestion_nomina")
def pagina_gestion_nomina():  
    return render_template("modules/nomina/gestion_nomina.html") 

# 4. Opción: Valores a Pagar
@app.route("/nomina/reporte_valores")
def pagina_reporte_valores():  
    return render_template("modules/nomina/reporte_valores.html") 

# 5. Opción: Reporte Cruzado
@app.route("/nomina/reporte-cruzado")
def pagina_reporte_cruzado():  
    return render_template("modules/nomina/reporte_cruzado.html")


# para contabilidad ul
@app.route("/contabilidad/cuenta")
def pagina_cuenta():
    return render_template("modules/contabilidad/cuenta.html")

@app.route("/contabilidad/comprobante")
def pagina_comprobante():
    return render_template("modules/contabilidad/comprobante.html")

@app.route("/contabilidad/balance")
def pagina_balance():
    return render_template("modules/contabilidad/balance.html")

@app.route("/contabilidad/estado_resultados")
def pagina_resultados():
    return render_template("modules/contabilidad/estado_resultados.html")

# para mantenimiento ul
@app.route("/mantenimiento/activos")
def pagina_activos():
    return render_template("modules/mantenimiento/activos.html")

@app.route("/mantenimiento/reporte_cruzado")
def pagina_reporte():
    return render_template("modules/mantenimiento/reporte_cruzado.html")

@app.route("/mantenimiento/reporte_valores")
def pagina_valores():
    return render_template("modules/mantenimiento/reporte_valores.html")

@app.route("/mantenimiento/mantenimiento")
def pagina_mantenimiento2():
    return render_template("modules/mantenimiento/mantenimiento.html")

#Biblioteca
@app.route("/biblioteca/libros")
def pagina_libros():
    return render_template("modules/biblioteca/libros.html")

@app.route("/biblioteca/asientos")
def pagina_asientos():
    return render_template("modules/biblioteca/asientos.html")

@app.route("/biblioteca/prestamos")
def pagina_prestamos():
    return render_template("modules/biblioteca/prestamos.html")

@app.route("/biblioteca/reportes")
def pagina_reportes():
    return render_template("modules/biblioteca/reportes.html")







if __name__ == "__main__":
    app.run(debug=True)