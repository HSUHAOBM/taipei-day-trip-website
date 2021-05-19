function loadapi() {
    // let src = "http://3.18.249.2:3000/api/attraction/"+Number(1)
    let src = "/api/booking"

    fetch(src, {
        headers: {
            "test": "getapidata"
        }
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        data = result;
        console.log(data)

        if (result.error) { goindex(); }

        if (data.data == null) {
            notaipdata();
        }
        if (data.data != null) {
            getaipdata();
            addbody();
        }


    });
}
loadapi();

function addbody() {
    document.querySelector('.righttext1').textContent = "台北一日遊：" + data.data.attraction.name;
    document.querySelector('.righttext2>div').textContent = data.data.date;
    if (data.data.time == "morning") {
        document.querySelector('.righttext3>div').textContent = "早上 9 點到下午 4 點";
        document.querySelector('.righttext4>div').textContent = "新台幣 2000 元";
        document.querySelector('.mainfinsh>a').textContent = "總價：新台幣 2000 元";

    }
    if (data.data.time == "afternoon") {
        document.querySelector('.righttext3>div').textContent = "下午 2 點到下午 9 點";
        document.querySelector('.righttext4>div').textContent = "新台幣 2500 元";
        document.querySelector('.mainfinsh>a').textContent = "總價：新台幣 2500 元";

    }
    document.querySelector('.righttext5>div').textContent = data.data.attraction.address;
    document.querySelector('.leftimg>img').src = data.data.attraction.image;
    document.querySelector('.leftimg>img').title = data.data.attraction.name;

}

function clearapi() {
    let url = "/api/booking "
    fetch(url, {
        method: "DELETE"
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        data = result;
        console.log(data)
        if (data.ok) {
            notaipdata()
            window.location.reload();

        }
    });
}

//無訂單資料
function notaipdata() {
    document.querySelector('.order').style.display = "none";
    document.querySelector('.mainfinsh').style.display = "none";

    document.querySelector('.infortext').hidden = false;

    document.querySelector('.maincenter').hidden = true;
    document.querySelector('.maincenter2').hidden = true;
    document.querySelector('#hr1').hidden = true;
    document.querySelector('#hr2').hidden = true;
    document.querySelector('#hr3').hidden = true;
    document.querySelector('.footer').style.height = "865px"

}

//有訂單資料
function getaipdata() {
    document.querySelector('.order').style.display = "flex";
    document.querySelector('.mainfinsh').style.display = "flex";

    document.querySelector('.infortext').hidden = true;

    document.querySelector('.maincenter').hidden = false;
    document.querySelector('.maincenter2').hidden = false;
    document.querySelector('#hr1').hidden = false;
    document.querySelector('#hr2').hidden = false;
    document.querySelector('#hr3').hidden = false;
    document.querySelector('.footer').style.height = "104px"

}