from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random 

app = Flask(__name__)

def scrape_comments(url, num_comments=5):
    driver = webdriver.Firefox()

    driver.get(url) 

    time.sleep(10)

    try:
        i = 0
        while i < num_comments: 
            load_more_comment = driver.find_element(By.XPATH,'//button[contains(text(), "Load more")]')
            load_more_comment.click()
            time.sleep(7)
            i += 1
    except Exception as e:
        pass

    user_names = []
    user_comments = []
    comment = driver.find_elements(By.CLASS_NAME,'_a9ym')
    for c in comment:
        container = c.find_element(By.CLASS_NAME,'_a9zr')
        name = container.find_element(By.CLASS_NAME,'_a9zc').text
        content = container.find_element(By.TAG_NAME,'span').text
        content = content.replace('\n', ' ').strip().rstrip()
        user_names.append(name)
        user_comments.append(content)

    user_names.pop(0)
    user_comments.pop(0)

    driver.close()

    return user_comments[:10]

def generate_new_comments(existing_comments, num_suggestions=5):
    suggestions = random.sample(existing_comments, min(num_suggestions, len(existing_comments)))
    return suggestions

@app.route('/comment_suggestions', methods=['POST'])
def comment_suggestions():
    if request.method == 'POST':
        data = request.get_json()
        url = data['url']
        num_comments = data.get('num_comments', 5)

        print("Received Instagram URL:", url)

        comments = scrape_comments(url, num_comments)
        
        generate_new = data.get('generate_new', 5)
        if generate_new:
            new_comments = generate_new_comments(comments)
            response = {
                'existing_comments': comments,
                'new_comment_suggestions': new_comments
            }
        else:
            response = {
                'comment_suggestions': comments
            }

        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
