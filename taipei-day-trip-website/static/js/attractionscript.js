//分析網址
var url = location.href;
url = url.split("/")
url = url[url.length - 1]

var list = document.getElementById('list');
var webimgcount = 0; //web img coun +2
let imhlength = 0; //web img
var buttons = document.getElementById('buttons').getElementsByTagName('span');
var index = 1; //圖片初始狀態
let data = null;
let timer;
let imgend = false;

function loadapi() {
    // let src = "http://3.18.249.2:3000/api/attraction/"+Number(1)
    // let src = "http://3.18.249.2:3000/api/attraction/" + Number(url)
    let src = "/api/attraction/" + Number(url)

    fetch(src).then(function(response) {
        return response.json();
    }).then(function(result) {
        data = result.data;
        // console.log(data)

        //圖片數量
        imhlength = (data.images.split('http://').length) - 1
        addbody();

        timestart();
        document.getElementById("loadgif").style.display = "none";


    });
}

function addbody() {


    console.log("圖片數量", imhlength)
    webimgcount = imhlength + 2
        // console.log(webimgcount)

    //設定List寬度
    list.style.width = 540 * (webimgcount) + 'px';
    // console.log("list.style.width",list.style.width)

    //最後一張
    let listimg_end = document.createElement("img")
    listimg_end.src = "http://" + data.images.split('http://')[imhlength].split(',')[0]
    list.appendChild(listimg_end)
        //中間1~end
    for (let i = 1; i < imhlength + 1; i++) {
        // console.log("i",i)
        // console.log("http://" + data.images[0].split('http://')[i].split(',')[0])
        let listimg = document.createElement("img")
        listimg.src = "http://" + data.images.split('http://')[i].split(',')[0]
        list.appendChild(listimg)
    }
    //第一張
    let listimg_one = document.createElement("img")
    listimg_one.src = "http://" + data.images.split('http://')[1].split(',')[0]
    list.appendChild(listimg_one)

    //根據圖片數量創片對應按鈕
    let buttons = document.getElementById('buttons')
    let spanbox = document.createElement("span");
    spanbox.id = 1
    spanbox.onclick = function() {
        let clickIndex = parseInt(this.getAttribute('id'));
        // console.log("clickIndex",clickIndex);
        gotoimg(clickIndex);
    };

    spanbox.className = "on"
    buttons.appendChild(spanbox);

    for (let i = 0; i < (imhlength - 1); i++) {
        // console.log(i)
        let spanbox = document.createElement("span");
        spanbox.id = i + 2
        spanbox.onclick = function() {
            let clickIndex = parseInt(this.getAttribute('id'));
            // console.log("clickIndex",clickIndex)
            gotoimg(clickIndex);
        };
        buttons.appendChild(spanbox);
    }

    let righttop = document.querySelector('.righttop');
    righttop.textContent = data.name;

    let rightmid = document.querySelector('.rightmid');
    rightmid.textContent = data.category + " at " + data.mrt;

    let information1 = document.querySelector('.information1');
    information1.textContent = data.description

    let information2 = document.querySelector('.information2');
    information2.textContent = "景點地址："

    let information3 = document.querySelector('.information3');
    information3.textContent = data.address

    let information4 = document.querySelector('.information4');
    information4.textContent = "交通方式："

    let information5 = document.querySelector('.information5');
    information5.textContent = data.transport



}

//場次選擇費用
function displayResult(text) {
    document.querySelector('.rightend5div').textContent = text;
}

// 自動撥放--------------------------------------

function timestart() {

    timer = setInterval(function() {
        play();
    }, 2800)
}

function play() {
    if (imgend) { prev(); } else {
        next();
    }

}

function stop() {
    clearInterval(timer);
}
list.onmouseover = stop;
list.onmouseout = timestart;
// -----------------------------------------------

window.onload = function() {
    loadapi();
    setinputdate();

}


function prev() {
    index -= 1;
    if (index < 1) {
        index = imhlength;
    }
    buttonsShow();

    animate(540);

}

function next() {

    index += 1;
    if (index > imhlength) {
        index = 1;
    }
    buttonsShow();
    animate(-540);
}




function animate(offset) {
    let newLeft = parseInt(list.style.left) + offset;
    list.style.left = newLeft + 'px';

    maxleft = -540 * (webimgcount - 2);
    if (newLeft == -540) {
        imgend = false;
        // console.log(imgend, "第一張") //第一張
    }
    if (newLeft == maxleft) {
        imgend = true;
        // console.log(imgend, "最後張") //最後張
    }

    if (newLeft > -540) {
        list.style.left = maxleft + 'px';

    }
    if (newLeft < maxleft) {
        list.style.left = -540 + 'px';
    }

}

//根據按鈕前往圖片
function gotoimg(clickIndex) {
    // console.log(clickIndex);
    list.style.left = -540 * (clickIndex) + 'px';
    // console.log(list.style.left);
    index = clickIndex;
    buttonsShow();
}
//清除切換鈕樣式
function buttonsShow() {
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].className == 'on') {
            buttons[i].className = '';
        }
    }
    //数组从0开始，故index需要-1
    buttons[index - 1].className = 'on';
}


let orderform = document.getElementById('order');
orderform.addEventListener('submit', function(event) {
    var orderformdata = new FormData(orderform);
    let formdata = {};
    event.preventDefault();


    if (orderformdata.get("time") == "morning") {
        formdata = {
            "attractionId": url,
            "date": orderformdata.get("date"),
            "time": orderformdata.get("time"),
            "price": 2000
        }
    }
    if (orderformdata.get("time") == "afternoon") {
        formdata = {
            "attractionId": url,
            "date": orderformdata.get("date"),
            "time": orderformdata.get("time"),
            "price": 2500
        }
    }

    let = urlbook = "/api/booking";
    // console.log(formdata);
    fetch(urlbook, {
        method: "POST",
        body: JSON.stringify(formdata),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        // console.log(result);
        if (result.error) {
            userboxshow();
        }
        if (result.ok) {
            gobooking()
        }

    })

})


function setinputdate() {
    let nowdate = new Date();
    nowdate.setDate(nowdate.getDate() + 3)
    let day = ("0" + nowdate.getDate()).slice(-2);
    let month = ("0" + (nowdate.getMonth() + 1)).slice(-2);
    let today = nowdate.getFullYear() + "-" + (month) + "-" + (day);

    const date = document.getElementById('date');
    date.setAttribute("value", today);

    // console.log(today)
}