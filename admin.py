from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql

app = Flask(__name__)

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_universitas'

# Koneksi ke database
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

@app.route("/")
def main() -> str:
    return render_template('index.html')

@app.route("/home")
def home() -> str:
    # Mengambil koneksi ke database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Menghitung jumlah dosen
    cursor.execute('SELECT COUNT(*) FROM dosen')  # Ganti 'dosen' dengan nama tabel dosen Anda
    jumlah_dosen = cursor.fetchone()[0]  # Ambil hasil pertama dari tuple

    # Menghitung jumlah pegawai
    cursor.execute('SELECT COUNT(*) FROM pegawai')  # Ganti 'pegawai' dengan nama tabel pegawai Anda
    jumlah_pegawai = cursor.fetchone()[0]  # Ambil hasil pertama dari tuple

    # Menghitung jumlah mahasiswa
    cursor.execute('SELECT COUNT(*) FROM mahasiswa')  # Ganti 'mahasiswa' dengan nama tabel mahasiswa Anda
    jumlah_mahasiswa = cursor.fetchone()[0]  # Ambil hasil pertama dari tuple

    # Menutup cursor dan koneksi
    cursor.close()
    connection.close()

    # Mengembalikan halaman dengan data jumlah dosen, pegawai, dan mahasiswa
    return render_template('index.html', 
                        jumlah_dosen=jumlah_dosen, 
                        jumlah_pegawai=jumlah_pegawai, 
                        jumlah_mahasiswa=jumlah_mahasiswa)

# READ: Menampilkan data Dosen
@app.route("/dataDosen", methods=['GET'])
def data_dosen() -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM dosen')  
    dosen = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('dataDosen.html', menu='data', submenu='dosenData', dosen=dosen)

# LIVE SEARCH: Mengambil data berdasarkan pencarian
@app.route("/searchDosen", methods=['POST'])
def search_dosen() -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    search_query = request.form.get('search_query', '')
    cursor.execute("SELECT * FROM dosen WHERE name LIKE %s OR jk LIKE %s OR jabatan LIKE %s OR tgl_gabung LIKE %s",
                   ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    
    dosen = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(dosen)


# CREATE: Menambah data Dosen
@app.route("/tambahDosen", methods=['GET', 'POST'])
def tambah_dosen() -> str:
    if request.method == 'POST':
        name = request.form['name']  # Ganti dengan nama kolom sesuai tabel Anda
        jk = request.form['jk']  # Jenis Kelamin
        jabatan = request.form['jabatan']  # Jabatan
        tgl_gabung = request.form['tgl_gabung']  # Tanggal Bergabung
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO dosen (name, jk, jabatan, tgl_gabung) VALUES (%s, %s, %s, %s)', 
                       (name, jk, jabatan, tgl_gabung))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('data_dosen'))
    return render_template('tambahDosen.html', menu='tambah', submenu='dosen')

# UPDATE: Mengedit data Dosen
@app.route("/editDosen/<int:id>", methods=['GET', 'POST'])
def edit_dosen(id) -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    if request.method == 'POST':
        name = request.form['name']
        jk = request.form['jk']
        jabatan = request.form['jabatan']
        tgl_gabung = request.form['tgl_gabung']
        cursor.execute('UPDATE dosen SET name = %s, jk = %s, jabatan = %s, tgl_gabung = %s WHERE id = %s', 
                       (name, jk, jabatan, tgl_gabung, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('data_dosen'))
    
    cursor.execute('SELECT * FROM dosen WHERE id = %s', (id,))
    dosen = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('editDosen.html', menu='edit', submenu='dosen', dosen=dosen)

# DELETE: Menghapus data Dosen
@app.route("/deleteDosen/<int:id>")
def delete_dosen(id) -> str:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM dosen WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('data_dosen'))


# READ: Menampilkan data mahasiswa
@app.route("/dataMahasiswa")
def data_mahasiswa() -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM mahasiswa')  # Ganti 'mahasiswa' dengan nama tabel Anda
    mahasiswa = cursor.fetchall()  # Mengambil data mahasiswa
    cursor.close()
    connection.close()
    return render_template('dataMahasiswa.html', menu='data', submenu='mahasiswa', mahasiswa=mahasiswa)

# CREATE: Menambah data mahasiswa
@app.route("/tambahMahasiswa", methods=['GET', 'POST'])
def tambah_mahasiswa() -> str:
    if request.method == 'POST':
        name = request.form['name']
        nim = request.form['nim']
        alamat = request.form['alamat']
        prodi = request.form['prodi']
        jk = request.form['jk']  # Jenis Kelamin
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO mahasiswa (name, nim, alamat, prodi, jk) VALUES (%s, %s, %s, %s, %s)', 
                       (name, nim, alamat, prodi, jk))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('data_mahasiswa'))
    return render_template('tambahMahasiswa.html', menu='tambah', submenu='mahasiswa')

# UPDATE: Mengedit data mahasiswa
@app.route("/editMahasiswa/<int:id>", methods=['GET', 'POST'])
def edit_mahasiswa(id) -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    if request.method == 'POST':
        name = request.form['name']
        nim = request.form['nim']
        prodi = request.form['prodi']
        alamat = request.form['alamat']
        jk = request.form['jk']
        cursor.execute('UPDATE mahasiswa SET name = %s, nim = %s, prodi = %s, alamat = %s, jk = %s WHERE id = %s', 
                       (name, nim, prodi, alamat, jk, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('data_mahasiswa'))
    
    cursor.execute('SELECT * FROM mahasiswa WHERE id = %s', (id,))
    mahasiswa = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('editMahasiswa.html', menu='edit', submenu='mahasiswa', mahasiswa=mahasiswa)

# DELETE: Menghapus data mahasiswa
@app.route("/deleteMahasiswa/<int:id>")
def delete_mahasiswa(id) -> str:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM mahasiswa WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('data_mahasiswa'))
# CRUD UNTUK PEGAWAI

# READ: Menampilkan data Pegawai
@app.route("/dataPegawai")
def data_pegawai() -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM pegawai')  # Mengambil data dari tabel pegawai
    pegawai = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('dataPegawai.html', menu='data', submenu='pegawaiData', pegawai=pegawai)

# CREATE: Menambah data Pegawai
@app.route("/tambahPegawai", methods=['GET', 'POST'])
def tambah_pegawai() -> str:
    if request.method == 'POST':
        name = request.form['name']  # Nama Pegawai
        jk = request.form['jk']  # Jenis Kelamin
        jabatan = request.form['jabatan']  # Jabatan
        alamat = request.form['alamat']  # Alamat
        tgl_gabung = request.form['tgl_gabung']  # Tanggal Bergabung
        
        connection = get_db_connection()
        cursor = connection.cursor()
        # Menggunakan tabel pegawai
        cursor.execute('INSERT INTO pegawai (name, jk, jabatan, alamat, tgl_gabung) VALUES (%s, %s, %s, %s, %s)', 
                       (name, jk, jabatan, alamat, tgl_gabung))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('data_pegawai'))
    return render_template('tambahPegawai.html', menu='tambah', submenu='pegawai')

# UPDATE: Mengedit data Pegawai
@app.route("/editPegawai/<int:id>", methods=['GET', 'POST'])
def edit_pegawai(id) -> str:
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    
    if request.method == 'POST':
        name = request.form['name']
        jk = request.form['jk']
        jabatan = request.form['jabatan']
        alamat = request.form['alamat']
        tgl_gabung = request.form['tgl_gabung']
        cursor.execute('UPDATE pegawai SET name = %s, jk = %s, jabatan = %s, alamat = %s, tgl_gabung = %s WHERE id = %s', 
                       (name, jk, jabatan, alamat, tgl_gabung, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('data_pegawai'))
    
    cursor.execute('SELECT * FROM pegawai WHERE id = %s', (id,))
    pegawai = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('editPegawai.html', menu='edit', submenu='pegawai', pegawai=pegawai)

# DELETE: Menghapus data Pegawai
@app.route("/deletePegawai/<int:id>")
def delete_pegawai(id) -> str:
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM pegawai WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('data_pegawai'))


if __name__ == "__main__":
    app.run(debug=True)
