from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main() -> str:
    return render_template('index.html')

@app.route("/home")
def home() -> str:
    return render_template('index.html')

@app.route("/dataDosen")
def data_dosen() -> str:
    return render_template('dataDosen.html',menu='data',submenu='dosenData')

@app.route("/dataPegawai")
def data_pegawai() -> str:
    return render_template('dataPegawai.html',menu='data',submenu='pegawaiData')

@app.route("/dataMahasiswa")
def data_mahasiswa() -> str:
    return render_template('dataMahasiswa.html',menu='data',submenu='mahasiswaData')

@app.route("/tambahDosen")
def tambah_dosen() -> str:
    return render_template('tambahDosen.html',menu='tambah', submenu='dosen')

@app.route("/tambahPegawai")
def tambah_pegawai() -> str:
    return render_template('tambahPegawai.html',menu='tambah',submenu='pegawai')

@app.route("/tambahMahasiswa")
def tambah_mahasiswa() -> str:
    return render_template('tambahMahasiswa.html',menu='tambah', submenu='mahasiswa')

if __name__ == "__main__":
    app.run(debug=True)
