from flask import Flask, render_template, request, redirect, url_for, session # digunakan untuk membuat dan mengelola aplikasi web dengan Flask di Python, dengan kemampuan untuk merender template, menangani permintaan dari pengguna, dan mengelola sesi pengguna.
import json #digunakan untuk pertukaran data di aplikasi web karena kemudahan membaca dan menulisnya, serta dukungan yang luas di berbagai bahasa pemrograman.
import pandas as pd # digunakan untuk analisis data, menyediakan struktur data yang mudah digunakan dan berbagai fungsi untuk bekerja dengan data terstruktur.

app = Flask(__name__) #menginisialisasi aplikasi Flask yang nantinya akan digunakan untuk menentukan rute (routes), menangani permintaan HTTP, dan melakukan berbagai tugas lainnya dalam aplikasi web yang akan dikembangkan.
app.secret_key = 'your_secret_key' #digunakan dalam pengembangan aplikasi web menggunakan kerangka kerja Flask di Python. Ini menetapkan kunci rahasia yang diperlukan untuk menjaga keamanan sesi dan data yang disimpan oleh aplikasi Flask.

# Fungsi untuk menyimpan data ke file JSON saat aplikasi dimulai
def save_data(): 
    with open('data.json', 'w') as json_file: 
        json.dump({'users': users_data, 'quiz': quiz_data, 'materials': learning_materials}, json_file) 

# Fungsi untuk memuat data dari file JSON saat aplikasi dimulai
def load_data(): 
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            return data.get('users', {}), data.get('quiz', []), data.get('materials', [])
    except FileNotFoundError:
        return {}, [], []


# Fungsi untuk menyimpan data pengguna ke file JSON
def save_users_data(): 
    with open('data.json', 'w') as json_file: 
        json.dump({'users': users_data, 'quiz': quiz_data, 'materials': learning_materials}, json_file) 

# Fungsi untuk menyimpan data kuis ke file JSON
def save_quiz_data(): 
    with open('quiz_data.json', 'w') as json_file: 
        json.dump(quiz_data, json_file) 

# Fungsi untuk menyimpan materi pembelajaran ke file JSON
def save_learning_materials(): 
    with open('learning_materials.json', 'w') as json_file: 
        json.dump(learning_materials, json_file)

# Load data saat aplikasi dimulai
users_data, quiz_data, learning_materials = load_data() 

# Definisi data pengguna jika belum ada
if not users_data: 
    users_data = { 
        'admin': {'password': 'admin123', 'role': 'guru'},
        'student': {'password': 'student123', 'role': 'siswa'}
        # Tambahkan data pengguna lainnya jika diperlukan
    }

# Data kuis
quiz_data = [
    
    # Tambahkan soal kuis lainnya jika diperlukan
]

# Dictionary untuk menyimpan skor pengguna
user_scores = {} 

# Route untuk halaman utama
@app.route('/') #digunakan dalam kerangka kerja Flask untuk menentukan URL yang akan ditangani oleh fungsi tertentu.
def home(): 
    if 'username' in session: 
        if session['role'] == 'guru': 
            return redirect(url_for('guru_dashboard'))
        elif session['role'] == 'siswa': 
            return redirect(url_for('siswa_dashboard')) 
    return render_template('login.html') 

# Fungsi login pengguna
def login_user(username, password):
    return username in users_data and password == users_data[username]['password']

# Route untuk proses login
@app.route('/login', methods=['POST'])
def login(): 
    username = request.form['username']
    password = request.form['password']

    if login_user(username, password):
        session['username'] = username
        session['role'] = users_data[username]['role']
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error='Username atau password salah')

# Route untuk dashboard guru
@app.route('/guru/dashboard')
def guru_dashboard(): 
    if 'username' in session and session['role'] == 'guru':
        return render_template('guru_dashboard.html', quiz_data=quiz_data, learning_materials=learning_materials)
    else:
        return redirect(url_for('home'))

# Route untuk menghapus kuis
@app.route('/guru/delete_quiz', methods=['GET', 'POST'])
def delete_quiz():
    if 'username' in session and session['role'] == 'guru':
        if request.method == 'POST':
            question_to_delete = request.form['question_to_delete']

            # Implementasi logika untuk menghapus kuis
            global quiz_data
            quiz_data = [quiz for quiz in quiz_data if quiz['question'] != question_to_delete]

            # Simpan data setelah menghapus kuis
            save_data()

            return redirect(url_for('guru_dashboard'))
        else:
            return render_template('delete_quiz.html')
    else:
        return redirect(url_for('home'))

# Route untuk menghapus materi pembelajaran
@app.route('/guru/delete_material', methods=['GET', 'POST'])
def delete_material():
    if 'username' in session and session['role'] == 'guru':
        if request.method == 'POST':
            material_title_to_delete = request.form['material_title_to_delete']

            # Implementasi logika untuk menghapus materi
            global learning_materials
            learning_materials = [material for material in learning_materials if material['title'] != material_title_to_delete]

            # Simpan data setelah menghapus materi
            save_data()

            return redirect(url_for('guru_dashboard'))
        else:
            return render_template('delete_material.html', learning_materials=learning_materials)
    else:
        return redirect(url_for('home'))

# Route untuk menambahkan pengguna baru
@app.route('/guru/add_user', methods=['GET', 'POST'])
def add_user(): 
    if 'username' in session and session['role'] == 'guru':
        if request.method == 'POST':
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            new_role = request.form['new_role']

            if new_username not in users_data:
                users_data[new_username] = {'password': new_password, 'role': new_role}
                save_users_data()  # Simpan data setelah perubahan
                return render_template('add_user.html', user_added=new_username)
            else:
                return render_template('add_user.html', error='Username sudah ada')
        else:
            return render_template('add_user.html')
    else:
        return redirect(url_for('home'))

# Route untuk menghapus pengguna
@app.route('/guru/delete_user', methods=['GET', 'POST'])
def delete_user():
    if 'username' in session and session['role'] == 'guru':
        if request.method == 'POST':
            # Handle logika penghapusan di sini
            username_to_delete = request.form['username_to_delete']

            if username_to_delete in users_data:
                del users_data[username_to_delete]
                save_users_data()  # Simpan data setelah menghapus pengguna

                # Redirect kembali ke Guru Dashboard setelah penghapusan
                return redirect(url_for('guru_dashboard'))
            else:
                error = 'Pengguna tidak ditemukan'
                return render_template('delete_user.html', error=error)

        else:
            # Render template delete_user.html untuk metode GET
            return render_template('delete_user.html')

    else:
        return redirect(url_for('home'))

# Route untuk menambahkan kuis baru
@app.route('/guru/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if 'username' in session and session['role'] == 'guru':
        if request.method == 'POST':
            question = request.form['question']
            options = request.form.getlist('options')
            answer = request.form['answer']

            quiz_data.append({"question": question, "options": options, "answer": answer})

            # Simpan data setelah menambahkan kuis
            save_data()

            return render_template('add_quiz.html', quiz_added=True)
        else:
            return render_template('add_quiz.html')
    else:
        return redirect(url_for('home'))


# Route untuk menambahkan materi pembelajaran baru
@app.route('/guru/add_material', methods=['GET', 'POST'])
def add_material(): 
    if 'username' in session and session['role'] == 'guru':
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            learning_materials.append({"title": title, "content": content})
            
            # Simpan data setelah menambahkan materi
            save_data()
            
            # Set pesan dalam session
            session['message'] = 'Data materi pembelajaran telah ditambah. Terima kasih!'
            
            return redirect(url_for('add_material'))  # Redirect ke halaman add_material.html
        else:
            return render_template('add_material.html')
    else:
        return redirect(url_for('home'))


# Route untuk dashboard siswa
@app.route('/siswa/dashboard')
def siswa_dashboard(): 
    if 'username' in session and session['role'] == 'siswa':
        return render_template('siswa_dashboard.html')
    else:
        return redirect(url_for('home'))

# Route untuk mengambil kuis
@app.route('/quiz', methods=['GET', 'POST'])
def take_quiz(): 
    if 'username' in session and session['role'] == 'siswa':
        if quiz_data:  # Periksa apakah ada soal kuis yang tersedia
            if request.method == 'GET':
                # Tampilkan soal kuis pertama
                question_index = 0
                return render_template('quiz_question.html', question=quiz_data[question_index], question_index=question_index)
            elif request.method == 'POST':
                # Tangani jawaban yang dikirim dan pindah ke soal berikutnya
                question_index = int(request.form['question_index'])
                user_answer = request.form['answer']

                # Simpan jawaban pengguna di sesi
                answer_key = f"user_answer_{question_index}"
                session[answer_key] = user_answer

                # Pindah ke soal berikutnya atau redirect ke halaman skor jika tidak ada lagi soal
                question_index += 1
                if question_index < len(quiz_data):
                    return render_template('quiz_question.html', question=quiz_data[question_index], question_index=question_index)
                else:
                    # Simpan data kuis ke file JSON
                    save_quiz_data()
                    return redirect(url_for('view_score'))
        else:
            # Tampilkan pesan jika tidak ada soal kuis yang tersedia
            return render_template('no_quiz.html')
    else:
        return redirect(url_for('home'))


# Route untuk menampilkan skor
@app.route('/score')
def view_score():
    if 'username' in session and session['role'] == 'siswa':
        username = session['username']

        # Dapatkan skor untuk pengguna yang sedang login
        user_score = calculate_user_score(username)

        # Dapatkan jawaban yang sudah dijawab oleh pengguna
        user_answers = []  # Simpan jawaban dalam bentuk tuple (pertanyaan, jawaban pengguna, jawaban benar)
        for index, question in enumerate(quiz_data):
            answer_key = f"user_answer_{index}"
            if answer_key in session:
                user_answer = session[answer_key]
                correct_answer = question['answer']
                user_answers.append((question['question'], user_answer, correct_answer))

        # Simpan data kuis ke file Excel
        save_quiz_data_excel(username)

        return render_template('score.html', user_score=user_score, user_answers=user_answers)
    else:
        return redirect(url_for('home'))

# Fungsi untuk menghitung skor pengguna
def calculate_user_score(username): 
    user_score = 0
    for index, question in enumerate(quiz_data):
        answer_key = f"user_answer_{index}"
        if answer_key in session:
            user_answer = session[answer_key]
            correct_answer = question['answer']
            if user_answer == correct_answer:
                user_score += 1

    # Simpan skor pengguna ke dalam dictionary user_scores
    user_scores[username] = user_score
    return user_score

# Fungsi untuk menyimpan data kuis ke file Excel
def save_quiz_data_excel(username): 
    quiz_responses = []

    for index, question in enumerate(quiz_data):
        answer_key = f"user_answer_{index}"
        if answer_key in session:
            user_answer = session[answer_key]
            correct_answer = question['answer']
            quiz_responses.append({
                'Username': username,
                'Quiz Number': index + 1,
                'Question': question['question'],
                'User Answer': user_answer,
                'Correct Answer': correct_answer
            })

    df = pd.DataFrame(quiz_responses)

    # Menyimpan DataFrame ke dalam file Excel
    excel_filename = f"quiz_responses_{username}.xlsx"
    df.to_excel(excel_filename, index=False)

# Route untuk menampilkan materi pembelajaran
@app.route('/materials')
def view_materials(): 
    if 'username' in session and session['role'] == 'siswa':
        return render_template('materials.html', learning_materials=learning_materials)
    else:
        return redirect(url_for('home'))

# Route untuk logout
@app.route('/logout')
def logout(): 
    session.pop('username', None)
    session.pop('role', None)
    session.clear()  # Membersihkan semua data session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)