from flask import Flask, render_template, url_for, redirect, request
import json
import jieba
import math
import numpy as np

with open('D:\\Tady\\Flask\\IDF.json', 'r', encoding="utf-8-sig") as fp:
    IDF = json.load(fp)
with open('D:\\Tady\\Flask\\QA.json', 'r', encoding="utf-8-sig") as fp:
    QA = json.load(fp)

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():

    print("ok")

    if request.method == 'POST':

        if request.values['send'] == '送出':
            user = request.values['content']
            word = user.replace(" ", "").rstrip("\n")
            seg_list = jieba.lcut(user)
            TF = {}
            count = 0
            for i in seg_list:
                count += 1
                if i not in TF:
                    TF[i] = 0
                TF[i] += 1
            for i in TF:
                TF[i] = round(TF[i]/count, 6)
            TF_IDF = {}
            a = 0
            for j in TF:
                if IDF.get(j) == None:
                    print("ERROR not found")
                    break
                TF_IDF[j] = TF[j]*IDF[j]
                a += np.dot(TF_IDF[j], TF_IDF[j])
            # a 內積
            a = math.pow(a, 0.5)
            max_ = [0, 0, 0]
            max_index = [0, 0, 0]
            for i in range(1, len(QA)):
                # b內積
                b = QA[i]["Inner_Production"]
                # print(b)
                a_dot_b = 0
                for word in TF_IDF:
                    # 相同的詞 不然長度不同
                    if word in QA[i]["Word"]:
                        #                    a              b
                        a_dot_b += QA[i]["Word"][word] * TF_IDF[word]
                if a_dot_b > 0:

                    result = a_dot_b/(a*b)

                    for ind in range(len(max_)):
                        if max_[ind] < result:
                            max_[ind] = result
                            max_index[ind] = i
                            break

            # print(max_index)
            print(QA[max_index[0]]["As"])
            print(QA[max_index[1]]["As"])
            print(QA[max_index[2]]["As"])

            return render_template('index.html', name=request.values['content'], RESULT1=QA[max_index[0]]["As"], RESULT2=QA[max_index[1]]["As"], RESULT3=QA[max_index[2]]["As"])
    return render_template('index.html', name="")


@app.route('/second', methods=['POST', 'GET'])
def test():

    if request.values['content'] != '':
        user = request.values['content']
        print(user)
        word = user.replace(" ", "").rstrip("\n")
        seg_list = jieba.lcut(user)
        TF = {}
        count = 0
        for i in seg_list:
            count += 1
            if i not in TF:
                TF[i] = 0
            TF[i] += 1
        for i in TF:
            TF[i] = round(TF[i]/count, 6)
        TF_IDF = {}
        a = 0
        for j in TF:
            if IDF.get(j) == None:
                print("ERROR not found")
                break
            TF_IDF[j] = TF[j]*IDF[j]
            a += np.dot(TF_IDF[j], TF_IDF[j])
        # a 內積
        a = math.pow(a, 0.5)
        max_ = [0, 0, 0]
        max_index = [0, 0, 0]
        for i in range(1, len(QA)):
            # b內積
            b = QA[i]["Inner_Production"]
            # print(b)
            a_dot_b = 0
            for word in TF_IDF:
                # 相同的詞 不然長度不同
                if word in QA[i]["Word"]:
                    #                    a              b
                    a_dot_b += QA[i]["Word"][word] * TF_IDF[word]
            if a_dot_b > 0:

                result = a_dot_b/(a*b)

                for ind in range(len(max_)):
                    if max_[ind] < result:
                        max_[ind] = result
                        max_index[ind] = i
                        break

        # print(max_index)
        print(QA[max_index[0]]["As"])
        print(QA[max_index[1]]["As"])
        print(QA[max_index[2]]["As"])

        return render_template('test.html', name=request.values['content'], RESULT1=QA[max_index[0]]["As"], RESULT2=QA[max_index[1]]["As"], RESULT3=QA[max_index[2]]["As"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
# 172.31.4.149
'''
          setTimeout(function()
          {
            let req = new XMLHttpRequest();
            req.open("GET", "http://210.70.175.13:5000/second");
            req.onload = function() {
              let respond1 =document.getElementById('id1');
              let respond2 =document.getElementById('id2');
              let respond3 =document.getElementById('id3');
              respond1.innerHTML=this.responseText;
              respond2.innerHTML=this.responseText;
              respond3.innerHTML=this.responseText;
            }
            req.send();
            console.log("I am the third log after 5 seconds");
           },2000);
          '''
