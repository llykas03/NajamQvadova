from flask import Flask, render_template, url_for, request, redirect, session,jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity
from functools import wraps
from flask_cors import CORS

global_message = None
global_stop = None

rola = 'user'
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['JWT_SECRET_KEY'] = 'tvoj_tajni_jwt_kljuc'
jwt = JWTManager(app)

#konekcija na bazu podataka#########
#konekcija na bazu podataka#########
#konekcija na bazu podataka#########

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"message": "Nemate dozvolu za pristup ovoj ruti."}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper



con = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password="",
    database='iznajmljivanjevozila'
)
cursor = con.cursor(dictionary=True)

#logika za klijent stranu###############
#logika za klijent stranu###############
#logika za klijent stranu###############
#logika za klijent stranu###############

#korisnici###########
#korisnici###########
#korisnici###########
#korisnici###########
@app.route('/login', methods=['POST'])
def loginForma():
       forma = request.json
       vrednosti = (
            forma['email'],
            
        )
       
       upit = '''
        select * from korisnici 
        where email=%s
       '''
       cursor.execute(upit,vrednosti)
       korisnik = cursor.fetchone()
       
       if korisnik and korisnik['lozinka'] == forma['password']:
        access_token = create_access_token(
            identity=korisnik['id'],
            additional_claims={"role": korisnik['rola']}
        )
        return jsonify({"message": "Uspešno ste se prijavili.","id":korisnik['id'], "access_token": access_token, "rola": korisnik['rola']}), 200
    
       else:
           
        return jsonify({"message": "Neispravni podaci za prijavu."}), 401

#get korisnik klijent
@app.route('/GETkorisnik/<int:id>', methods=['GET'])
@jwt_required()
@role_required(["administrator","user"])     
def getKorisnik(id) :
    
    if request.method == 'GET':
        upit = "select * from korisnici WHERE ID=%s"
        IDD=(id, )
        cursor.execute(upit,IDD)
        korisnik = cursor.fetchone()
        
        if not korisnik:
            return "Korisnik nije pronađen" + str(id), 404
        return  jsonify(korisnik), 200
    

#get vozilo jedno
@app.route('/GETvozilo/<int:id>', methods=['GET'])
@jwt_required()
@role_required(["administrator"])     
def getvozilo(id) :
    
    if request.method == 'GET':
        upit = "select * from vozila WHERE ID=%s"
        IDD=(id, )
        cursor.execute(upit,IDD)
        korisnik = cursor.fetchone()
        
        if not korisnik:
            return "vozilo nije pronađen" + str(id), 404
        return  jsonify(korisnik), 200

#get vozila klijent
@app.route('/vozilaa', methods=['GET'])
@jwt_required()
@role_required(["administrator","user"]) 
def render_vozilaa():
    upit = '''select * from vozila'''
    cursor.execute(upit)
    vozila = cursor.fetchall()
    return jsonify(vozila),200


#iznajmljivanje kvada
@app.route('/dodaj_rezervaciju', methods=['POST'])
@jwt_required()
@role_required(["administrator","user"])
def dodaj_rezervaciju():
    data = request.json
    global global_message
    if not data:
        return jsonify({"error": "Nema podataka"}), 400
    
    idVozila = data.get("idVozila")
    idKorisnika = data.get("idKorisnika")
    satnica = data.get("satnica")
    
    if not all([idVozila, idKorisnika, satnica]):
        return jsonify({"error": "Nedostaju podaci"}), 400
    
    ##########################
    #korisnikid,kvadoviid,satnica
    #########################
    
    formatirani_string = f"{idKorisnika},{idVozila},{satnica}"
    global_message = str(formatirani_string)
    print(formatirani_string)
    
    
    upit = """
        UPDATE vozila
        SET statusVozila = 'Zauzeto',
        satnicaUkupna = satnicaUkupna+%s,
        brojIznajmljivanja=brojIznajmljivanja+1        
        WHERE id = %s;
        """
    upit1 =  """
        INSERT INTO istorija_iznajmljivanja (korisnik_id, kvad_id)
        VALUES (%s, %s)
        """
    upit2="""
        UPDATE korisnici
        SET trenutniKorisnik = %s
        WHERE id = %s
    """
    
    vrednosti=(satnica,idVozila)
    vrednosti1=(idKorisnika,idVozila)
    vrednosti2=(idVozila,idKorisnika)
    
    
    try:
            cursor.execute(upit, vrednosti)
            con.commit()
    except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            con.rollback()
    try:
            cursor.execute(upit1, vrednosti1)
            con.commit()
    except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            con.rollback()
    try:
            cursor.execute(upit2, vrednosti2)
            con.commit()
    except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            con.rollback()
    
    
    tuple = (idVozila, )
    kreditu = """select cenaRadnogSata from vozila where id = %s"""
    cursor.execute(kreditu, tuple)
    k = cursor.fetchone()
    korisniku = """
    
        UPDATE korisnici
        SET kredit = kredit-(%s*%s)
        WHERE id = %s
    
    """
    cursor.execute(korisniku,(k['cenaRadnogSata'],satnica,idKorisnika))
    con.commit()
    
    
    return jsonify({"message": "Rezervacija uspešno dodata", "idVozila": idVozila, "idKorisnika": idKorisnika, "satnica": satnica}), 201


#vozila admin
@app.route('/admin-vozila', methods=['GET'])
@jwt_required()
@role_required(["administrator"])
def render_vozila_admin():
    upit = '''select * from vozila'''
    cursor.execute(upit)
    vozila = cursor.fetchall()
    return jsonify(vozila)
#vozilo brisanje admin
@app.route('/admin-vozila-brisanje/<int:id>', methods=['POST'])
@jwt_required()
@role_required(["administrator"])
def vozilo_brisanjee(id):
    
    IDD=(id, )
    upit = '''DELETE FROM vozila
              WHERE id = %s;
            '''
    cursor.execute(upit,IDD)
    con.commit()
    return jsonify("uspesno obrisano vozilo")
#izmena vozila  
@app.route('/admin-vozilo-izmena/<int:id>', methods=['POST'])  
@jwt_required()
@role_required(["administrator"])     
def vozilo_izmenaaa(id) :
        
        upit = """
        update vozila SET
        ime=%s,
        boja=%s,
        registracija=%s,
        gorivo=%s,
        motor=%s,
        kubikaza=%s,
        konjskeSnage=%s,
        statusVozila=%s,
        godinaProizvodnje=%s,
        cenaRadnogSata = %s
        where id = %s
        """
        
        forma = request.json
        
        vrednosti = (
            forma['ime'],
            forma['boja'],
            forma['registracija'],
            forma['gorivo'],
            forma['motor'],
            forma['kubikaza'],
            forma['konjskeSnage'],
            forma['statusVozila'],
            forma['godinaProizvodnje'],
            forma['cenaRadnogSata'],
            id
        )
        
        
        cursor.execute(upit,vrednosti)
        con.commit()
        return jsonify("uspesno izmenjeno vozilo")   
#dodavanje vozila
@app.route('/admin-vozilo-novo', methods=['POST'])
@jwt_required()
@role_required(["administrator"])
def vozilo_noviia():
    if request.method == 'POST':
       
        forma = request.json
        
        vrednosti = (
            forma['ime'],
            forma['boja'],
            forma['registracija'],
            forma['gorivo'],
            forma['kubikaza'],
            forma['motor'],
            forma['konjskeSnage'],
            forma['godinaProizvodnje'],
            forma['statusVozila'],
            forma['cenaRadnogSata'],
            0,
            0
        )

        upit = '''INSERT INTO vozila (ime,boja,registracija,gorivo,kubikaza,motor,konjskeSnage,godinaProizvodnje,statusVozila,cenaRadnogSata,brojIznajmljivanja,satnicaUkupna)
                  VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s,%s);'''
                  
        cursor.execute(upit,vrednosti)
        con.commit()
                 
        return  jsonify("uspesno dodato vozilo")

######################
######################
######################
#korisnici admin

@app.route('/admin-korisnici', methods=['GET'])
@jwt_required()
@role_required(["administrator"])
def render_korisnici_admin():
    upit = '''select * from korisnici'''
    cursor.execute(upit)
    korisnici = cursor.fetchall()
    return jsonify(korisnici)
#brisanje korisnika admin
@app.route('/admin-k-brisanje/<int:id>', methods=['POST'])
@jwt_required()
@role_required(["administrator"])
def korisnik_brisanje_admin(id):
    
    IDD=(id, )
    upit = '''DELETE FROM korisnici
              WHERE id = %s;
            '''
    cursor.execute(upit,IDD)
    con.commit()
    return jsonify("uspesno obrisan korisnik")
#izmena korisnika admin
@app.route('/admin-k-izmena/<int:id>', methods=['POST'])
@jwt_required()
@role_required(["administrator"])
def korisnik_izmena_admin(id) :
    
    if request.method == 'POST':
        upit = """
        update KORISNICI SET
        ime=%s,
        srednje_ime=%s,
        prezime=%s,
        email=%s,
        lozinka=%s,
        jmbg=%s,
        broj_licne_karte=%s,
        kredit=%s,
        rola=%s
        where id = %s
        """
        
        forma = request.json
        
        vrednosti = (
            forma['ime'],
            forma['srednje_ime'],
            forma['prezime'],
            forma['email'],
            forma['lozinka'],
            forma['jmbg'],
            forma['broj_licne_karte'],
            forma['kredit'],
            forma['rola'],
            id
        )
        
        cursor.execute(upit,vrednosti)
        con.commit()
        return jsonify("uspesno izmenjen korisnik")
#dodavanje korisnika
@app.route('/korisnik-novii', methods=['POST'])
def korisnik_novii():
    if request.method == 'POST':
        
        forma = request.json
        vrednosti = (
            forma['ime'],
            forma['srednje_ime'],
            forma['prezime'],
            forma['email'],
            forma['lozinka'],
            forma['jmbg'],
            forma['broj_licne_karte'],
            forma['kredit'],
            forma['rola'], 
        )
        upit = '''INSERT INTO KORISNICI (ime,srednje_ime,prezime,email,lozinka,jmbg,broj_licne_karte,kredit,rola)
                  VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s);'''
                  
        cursor.execute(upit,vrednosti)
        con.commit()          
        return  jsonify("uspesno kreiran korisnik")






#OVO DOLE SE NE KORISTI SLUZI RADI TESTIRANJA
#jinja sintaksa#############
############################
###########################
###########################
###########################
##########################
@app.route('/korisnici', methods=['GET'])
def render_korisnici():
    upit = '''select * from korisnici'''
    cursor.execute(upit)
    korisnici = cursor.fetchall()
    return render_template('korisnici.html', korisnici = korisnici)
        
@app.route('/korisnik-brisanje/<id>', methods=['POST'])
def korisnik_brisanje(id):
    
    IDD=(id, )
    upit = '''DELETE FROM korisnici
              WHERE id = %s;
            '''
    cursor.execute(upit,IDD)
    con.commit()
    return redirect(url_for('render_korisnici'))
     
@app.route('/korisnik-izmena/<id>', methods=['GET','POST'])       
def korisnik_izmena(id) :
    
    if request.method == 'GET':
        upit = "select * from korisnici WHERE ID=%s"
        IDD=(id, )
        cursor.execute(upit,IDD)
        korisnik = cursor.fetchone()
        if not korisnik:
            return "Korisnik nije pronađen" + str(id), 404
        return  render_template('korisnik-izmena.html', korisnik = korisnik)

    if request.method == 'POST':
        
        
        upit = """
        update KORISNICI SET
        ime=%s,
        srednje_ime=%s,
        prezime=%s,
        email=%s,
        lozinka=%s,
        jmbg=%s,
        broj_licne_karte=%s,
        kredit=%s,
        rola=%s
        where id = %s
        """
        
        forma = request.form
        vrednosti = (
            forma['ime'],
            forma['srednje_ime'],
            forma['prezime'],
            forma['email'],
            forma['lozinka'],
            forma['jmbg'],
            forma['broj_licne_karte'],
            forma['kredit'],
            forma['rola'],
            id
        )
        
        cursor.execute(upit,vrednosti)
        con.commit()
        return redirect(url_for('render_korisnici'))    
    
@app.route('/korisnik-novi', methods=['GET', 'POST'])
def korisnik_novi():
    if request.method == 'GET':
       return render_template('korisnik-novi.html')
   
    if request.method == 'POST':
        
        forma = request.form
        vrednosti = (
            forma['ime'],
            forma['srednje_ime'],
            forma['prezime'],
            forma['email'],
            forma['lozinka'],
            forma['jmbg'],
            forma['broj_licne_karte'],
            forma['kredit'],
            forma['rola'], 
        )
        upit = '''INSERT INTO KORISNICI (ime,srednje_ime,prezime,email,lozinka,jmbg,broj_licne_karte,kredit,rola)
                  VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s);'''
                  
        cursor.execute(upit,vrednosti)
        con.commit()          
        return  redirect(url_for('render_korisnici'))   

@app.route('/korisnik-pretraga', methods=['POST'])
def korisnik_pretraga():
    forma = request.form

    vrednosti=(
        forma['ime'],
        forma['prezime'],
        forma['jmbg']
    )
    
    upit='''
            SELECT * FROM korisnici
            WHERE 
            ime = %s 
            OR prezime = %s
            OR jmbg = %s
        '''
    cursor.execute(upit,vrednosti)
    korisnici = cursor.fetchall()
    if not korisnici:
        return redirect(url_for('render_korisnici'))
    else:
        return render_template('korisnici.html', korisnici = korisnici)

@app.route('/istorija/<id>', methods=['GET'])
def render_istorija(id):
    
    predupit = """
        select ime,prezime,jmbg from korisnici where id = %s
    """
    
    cursor.execute(predupit,(id, ))
    Korisnik = cursor.fetchall();
    
    upit = """
    select v.* from istorija_iznajmljivanja i inner join vozila v on i.kvad_id=v.id
    where i.korisnik_id = %s
    """
    IDD = (id, )
    
    cursor.execute(upit,IDD)
    vozila = cursor.fetchall()
    
    return render_template('istorija.html', vozila = vozila, Korisnik = Korisnik)
#kvadovi####
#kvadovi####
#kvadovi####
#kvadovi###
@app.route('/vozila', methods=['GET'])
def render_vozila():
    upit = '''select * from vozila'''
    cursor.execute(upit)
    vozila = cursor.fetchall()
    return render_template('vozila.html', vozila = vozila)
        
@app.route('/vozila-brisanje/<id>', methods=['POST'])
def vozilo_brisanje(id):
    
    IDD=(id, )
    upit = '''DELETE FROM vozila
              WHERE id = %s;
            '''
    cursor.execute(upit,IDD)
    con.commit()
    return redirect(url_for('render_vozila'))
     
@app.route('/vozilo-izmena/<id>', methods=['GET','POST'])       
def vozilo_izmena(id) :
    
    if request.method == 'GET':
        upit = "select * from vozila WHERE ID=%s"
        IDD=(id, )
        cursor.execute(upit,IDD)
        vozila = cursor.fetchone()
        if not vozila:
            return "vozilo nije pronađeno" + str(id), 404
        return  render_template('vozilo-izmena.html', vozilo = vozila)

    if request.method == 'POST':
        
        
        upit = """
        update vozila SET
        ime=%s,
        boja=%s,
        registracija=%s,
        gorivo=%s,
        motor=%s,
        kubikaza=%s,
        konjskeSnage=%s,
        statusVozila=%s,
        godinaProizvodnje=%s,
        cenaRadnogSata = %s
        where id = %s
        """
        
        forma = request.form
        print(forma)
        vrednosti = (
            forma['ime'],
            forma['boja'],
            forma['registracija'],
            forma['gorivo'],
            forma['motor'],
            forma['kubikaza'],
            forma['konjskeSnage'],
            forma['statusVozila'],
            forma['godinaProizvodnje'],
            forma['cenaRadnogSata'],
            id
        )
        print(vrednosti)
        
        cursor.execute(upit,vrednosti)
        con.commit()
        return redirect(url_for('render_vozila'))    
    
@app.route('/vozilo-novi', methods=['GET', 'POST'])
def vozilo_novi():
    if request.method == 'GET':
       return render_template('vozilo-novi.html')
   
    if request.method == 'POST':
       
        forma = request.form
        print(forma)
        vrednosti = (
            forma['ime'],
            forma['boja'],
            forma['registracija'],
            forma['gorivo'],
            forma['kubikaza'],
            forma['motor'],
            forma['konjskeSnage'],
            forma['godinaProizvodnje'],
            forma['statusVozila'],
            forma['cenaRadnogSata'],
            0,
            0
        )
        print(vrednosti)
        upit = '''INSERT INTO vozila (ime,boja,registracija,gorivo,kubikaza,motor,konjskeSnage,godinaProizvodnje,statusVozila,cenaRadnogSata,brojIznajmljivanja,satnicaUkupna)
                  VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s,%s);'''
                  
        cursor.execute(upit,vrednosti)
        con.commit()
        print('ceka je konj')          
        return  redirect(url_for('render_vozila'))   

@app.route('/vozilo-pretraga', methods=['POST'])
def vozilo_pretraga():
    forma = request.form

    vrednosti=(
        forma['ime'],
        forma['registracija'],
        forma['gorivo'],
        forma['statusVozila']
    )
    print(vrednosti)
    
    upit='''
            SELECT * FROM vozila
            WHERE 
            ime = %s 
            OR registracija = %s
            OR gorivo = %s
            OR statusVozila = %s
        '''
    cursor.execute(upit,vrednosti)
    vozila = cursor.fetchall()
    if not vozila:
        return redirect(url_for('render_vozila'))
    else:
        return render_template('vozila.html', vozila = vozila)


@app.route('/index', methods=['GET'])
def render_index():
    return render_template("index.html");


####################################################
####################################################
######################################################
#######################################################
######################################################
######################################################


#logika za esp32######################
#logika za esp32######################
#logika za esp32######################
#logika za esp32######################

@app.route('/iznajmiKvad', methods=['GET'])
def get_message():
    global global_message

    if global_message is None:
        return jsonify({"message": "Nema poruke"}), 204  # 204 - No Content

    # Ako postoji poruka, šaljemo je ESP32
    response = jsonify({"message": global_message})
    global_message = None
    return response   

@app.route("/stopVozilo", methods=['GET'])
def stopVozilo():
    global global_stop

    if global_stop is None:
        return jsonify({"message": "Nema stop"}), 204  # 204 - No Content

    # Ako postoji poruka, šaljemo je ESP32
    response = jsonify({"message": global_stop})

    # Nakon slanja poruke, resetujemo global_message da sprečimo ponovno slanje iste poruke
    global_stop = None  

    return response   

@app.route('/isteklovreme', methods=['POST'])
def receive_message():
    # Preuzima JSON podatke iz zahteva
    data = request.get_json()

    # Provera da li je poruka prisutna u JSON-u
    if not data or 'message' not in data:
        return jsonify({"error": "Nema poruke u zahtevu"}), 400  # 400 - Bad Request

    # Izdvajanje poruke iz JSON-a
    message = data['message']
    
    # Ispisivanje poruke u konzolu
    
    predupit = """select trenutniKorisnik from korisnici
                  where id = %s"""
    try:
            cursor.execute(predupit, (message, ))
            k = cursor.fetchall()
            con.commit()
            kvadId = k[0]['trenutniKorisnik']
    except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            con.rollback()  # Vraća promene u slučaju greške              
                  
    
    upit = """ 
            UPDATE vozila
            SET statusVozila = 'Slobodno'
            WHERE id = %s;
        """

    upit1 = """    
            UPDATE korisnici
            SET trenutniKorisnik = NULL
            WHERE id = %s;

        """
        
    try:
            cursor.execute(upit, (kvadId, ))
            con.commit()
    except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            con.rollback()  # Vraća promene u slučaju greške
    try:
            cursor.execute(upit1, (message, ))
            con.commit()
    except Exception as e:
            print(f"Greška pri izvršavanju upita: {e}")
            con.rollback()  # Vraća promene u slučaju greške

        

    return jsonify({"status": "Poruka primljena kvadSTOPIRAN", "message": message}), 200

#logika za esp32######################
#logika za esp32######################
#logika za esp32######################
#logika za esp32######################


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)  # Pokretanje Flask aplikacije
