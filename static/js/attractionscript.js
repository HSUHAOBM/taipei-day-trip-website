//分析網址
var url = location.href;
// console.log(url)
url=url.split("/")
url=url[url.length-1]
// console.log(url)
var list = document.getElementById('list');
var webimgcount=0;

function loadapi() {
    data=null;
    // let src = "http://3.18.249.2:3000/api/attraction/"+Number(1)
    let src = "http://3.18.249.2:3000/api/attraction/"+Number(url)
    
    fetch(src).then(function (response) {
        return response.json();
    }).then(function (result) {
        data = result.data;
        console.log(data)
        addbody();
    });
}

function addbody(){

    //圖片數量
    let imhlength=data.images[0].split('http://').length
    // console.log("圖片數量",imhlength-1)
    webimgcount=imhlength-1+2
    console.log(webimgcount)

    //設定List寬度
    list.style.width=540*(webimgcount)+ 'px';
    console.log("list.style.width",list.style.width)

    //最後一張
    let listimg_end = document.createElement("img")
    listimg_end.src="http://" + data.images[0].split('http://')[imhlength-1].split(',')[0]
    list.appendChild(listimg_end)
    //中間1~end
    for (let i=1;i< imhlength;i++){
        // console.log("http://" + data.images[0].split('http://')[i].split(',')[0])
            let listimg = document.createElement("img")
            listimg.src="http://" + data.images[0].split('http://')[i].split(',')[0]
            list.appendChild(listimg)
    }
    //第一張
    let listimg_one = document.createElement("img")
    listimg_one.src="http://" + data.images[0].split('http://')[1].split(',')[0]
    list.appendChild(listimg_one)


    let righttop=document.querySelector('.righttop');
    righttop.textContent=data.name;

    let rightmid=document.querySelector('.rightmid');
    rightmid.textContent=data.category+" at "+data.mrt;

    let information1=document.querySelector('.information1');
    information1.textContent=data.description

    let information2=document.querySelector('.information2');
    information2.textContent="景點地址："

    let information3=document.querySelector('.information3');
    information3.textContent=data.address

    let information4=document.querySelector('.information4');
    information4.textContent="交通方式："
    
    let information5=document.querySelector('.information5');
    information5.textContent=data.transport
}

//場次選擇費用
function displayResult(text){
   document.querySelector('.rightend5div').textContent=text;
}


window.onload = function() {
    loadapi()
    let prev = document.getElementById('prev');
    let next = document.getElementById('next');

    function animate(offset) {
        let newLeft = parseInt(list.style.left) + offset;
        list.style.left = newLeft + 'px';
        maxleft=-540*(webimgcount-2)
        console.log(maxleft)
        if (newLeft > -540) {
            list.style.left = maxleft + 'px';
        }
        if (newLeft < maxleft) {
            list.style.left = -540 + 'px';
        }
    }

    prev.onclick = function() {   
        animate(540);
    }
    next.onclick = function() {  
        animate(-540);
    }
}