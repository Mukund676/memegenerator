from connection import get_db

def setup_memes():
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''create table if not exists memes
    (
        "userId" integer,
        "memeImage" Text,
        "memeId" integer primary key autoincrement,
        foreign key(userId) references users(userId)
    )''')

def save_meme(user_id, image):
    connection = get_db()
    sql = connection.cursor()
    sql.execute('''insert into memes (userId, memeImage) values
                  (?, ?)''', [user_id, image])
    connection.commit()

def get_memes():
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('''select memes.memeImage, memes.memeId, users.username,
                            profile.FirstName, profile.LastName from memes
                            join users using(userId)
                            join profile using(userId)
                            order by memes.memeId desc''')
    return result.fetchall()

def my_memes(user_id):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('select * from memes where userId = ?', [user_id])
    rows = result.fetchall()
    return rows

def delete_meme(meme_id):
    connection = get_db()
    sql = connection.cursor()
    result = sql.execute('delete from memes where memeId = ?', [meme_id])
    connection.commit()
