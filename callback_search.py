# CALLBACK | An Recall Open Source Clone
#
# CAUTION!
# NOT SAFE TO USE! THIS SCRIPT DOES NOT ENCRYPT ANY STORED DATA.

import sqlite3

def search_images(keyword):
    conn = sqlite3.connect('screenshots.db')
    cursor = conn.cursor()
    keyword = keyword.lower()
    cursor.execute("SELECT image_path FROM screenshots WHERE tokens LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results]

# Query for keyword
keyword = "python"
image_paths  = search_images(keyword)

# List found images
for path in image_paths:
    print(path)
