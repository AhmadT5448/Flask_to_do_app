from flask import Flask,render_template,request,jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('to_do_list.sqlite')
    except sqlite3.Error as e:
        print(e)
    return(conn)


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        subject_list = request.form.get('subject')
        sql = """INSERT INTO to_do_list (to_do)
                VALUES (?)"""
        cursor = conn.execute(sql, (subject_list,))
        conn.commit()

    cursor.execute("SELECT * FROM to_do_list")
    tasks = cursor.fetchall()
    return render_template('home.html', task=tasks)

    
@app.route('/show', methods=['GET', 'POST'])
def show():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM to_do_list")
    tasks = cursor.fetchall()
    return render_template('show.html', task = tasks)

        
    

#CRUD operations down below

@app.route('/test',methods=['GET', 'POST'])
def show_list(): 
     conn = db_connection()
     cursor = conn.cursor()
     if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM to_do_list")
        list = [
            dict(id = row[0], to_do = row[1])
            for row in cursor.fetchall()
        ]
        if list is not None:
            return jsonify(list)

     if request.method == 'POST':
            new_task = request.form['to_do']
            sql = """INSERT INTO to_do_list (to_do)
            VALUES (?)"""
            cursor = conn.execute(sql, (new_task,))
            conn.commit()
            return f"task with the id {cursor.lastrowid} created successfully", 201

@app.route('/tests/<int:sr>', methods=['GET', 'PUT', 'DELETE'])
def single_task(sr):
    conn = db_connection()
    cursor = conn.cursor()
    pointed_task = None
    if request.method == 'GET':
       cursor.execute("SELECT * FROM to_do_list WHERE sr=?", (sr,))
       tasks = cursor.fetchall()
       for q in tasks:
            pointed_task = q
       if pointed_task is not None:
            return jsonify(pointed_task)
       else:
            return"somthing went wrong", 404

    if request.method == 'PUT':
        sql="""UPDATE to_do_list SET to_do=? WHERE sr=?"""
        new_to_do = request.form['to_do']
        updated_task = {
            "sr" : sr,
            "to_do" : new_to_do
        }
        conn.execute(sql, (new_to_do, sr))
        conn.commit()
        return jsonify(updated_task)


    if request.method == 'DELETE':
        sql = """DELETE FROM to_do_list WHERE sr=?"""
        conn.execute(sql, (sr,))
        conn.commit()
        return "The task with the sr: {} has been deleted".format(sr),200



if __name__ == '__main__':
    app.run(debug=True)