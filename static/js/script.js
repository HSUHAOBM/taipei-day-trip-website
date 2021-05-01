
var div_main = document.createElement("div");
div_main.className = "main";
var div_content = document.createElement("div");
div_content.className = "content";
div_main.appendChild(div_content);
var warp = document.querySelector('.warp');
warp.appendChild(div_main)


var page = 0;
var keyword = "";
var checkonload = true;
nextpage = null;

//讀取
window.onload = function () {
    let src = "http://3.18.249.2:3000/api/attractions?page=" + String(page) + "&keyword=" + keyword;

    fetch(src).then(function (response) {
        return response.json();
    }).then(function (result) {
        // console.log(result.data.length)

        for (let i = 0; i < result.data.length; i++) {
            // console.log("http://" +result.data[i].images[0].split('http://')[1].split(',')[0])
            let div_box = document.createElement("div")
            div_box.className = "box";
            div_content.appendChild(div_box)

            let div_imgbox = document.createElement("div")
            div_imgbox.className = "imgbox";
            div_box.appendChild(div_imgbox);

            let img_imgboximg = document.createElement("img")
            img_imgboximg.className = "imgboximg";
            img_imgboximg.src = "http://" + result.data[i].images[0].split('http://')[1].split(',')[0];
            div_imgbox.appendChild(img_imgboximg);
            // name
            let div_text1 = document.createElement("div")
            div_text1.className = "text1";
            div_text1.textContent = result.data[i].name
            div_box.appendChild(div_text1);

            let div_textbox = document.createElement("div")
            div_textbox.style = "display: flex;";
            div_box.appendChild(div_textbox);

            //mrt
            let div_text2 = document.createElement("div")
            div_text2.className = "text2";
            div_text2.textContent = result.data[i].mrt
            div_textbox.appendChild(div_text2);

            //category
            let div_text3 = document.createElement("div")
            div_text3.className = "text3";
            div_text3.textContent = result.data[i].category
            div_textbox.appendChild(div_text3);

        }
        nextpage = result.nextpage
        console.log("nextpage", nextpage)

    });

}
//新增
function adddata() {
    let src = "http://3.18.249.2:3000/api/attractions?page=" + String(page) + "&keyword=" + keyword;
    fetch(src).then(function (response) {
        return response.json();
    }).then(function (result) {
        // console.log(result.data.length)
        if (result.error) {
            alert("無資料");
            history.go(-1);
        }
        for (let i = 0; i < result.data.length; i++) {
            // console.log("http://" +result.data[i].images[0].split('http://')[1].split(',')[0])
            let div_box = document.createElement("div")
            div_box.className = "box";
            div_content.appendChild(div_box)

            let div_imgbox = document.createElement("div")
            div_imgbox.className = "imgbox";
            div_box.appendChild(div_imgbox);

            let img_imgboximg = document.createElement("img")
            img_imgboximg.className = "imgboximg";
            img_imgboximg.src = "http://" + result.data[i].images[0].split('http://')[1].split(',')[0];
            div_imgbox.appendChild(img_imgboximg);
            // name
            let div_text1 = document.createElement("div")
            div_text1.className = "text1";
            div_text1.textContent = result.data[i].name
            div_box.appendChild(div_text1);

            let div_textbox = document.createElement("div")
            div_textbox.style = "display: flex;";
            div_box.appendChild(div_textbox);

            //mrt
            let div_text2 = document.createElement("div")
            div_text2.className = "text2";
            div_text2.textContent = result.data[i].mrt
            div_textbox.appendChild(div_text2);

            //category
            let div_text3 = document.createElement("div")
            div_text3.className = "text3";
            div_text3.textContent = result.data[i].category
            div_textbox.appendChild(div_text3);

        }

        checkonload = true;
        nextpage = result.nextpage
        console.log("nextpage", nextpage)

    });
}

//畫面捲動監聽
window.addEventListener('scroll', function () {
    let webwarp = document.querySelector('.warp');
    // console.log("網頁高度",webwarp.scrollHeight)
    // console.log("到網頁頂端的距離",window.pageYOffset)//捲動
    // console.log("視窗高度",window.innerHeight)//視窗
    if (10 > (webwarp.scrollHeight - window.pageYOffset - window.innerHeight) & checkonload == true & nextpage != null) {
        checkonload = false;
        page += 1;
        adddata()
    }
})

//取得關鍵字
function addkeydata() {
    page = 0;
    let inputkeyword = document.querySelector('.searchtext');
    console.log(inputkeyword.value)
    keyword = inputkeyword.value
    while (div_content.firstChild) {
        div_content.removeChild(div_content.firstChild);
    }
    adddata();
}
