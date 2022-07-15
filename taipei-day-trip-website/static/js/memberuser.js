let textcontrol = true;
let logbtn = document.querySelector('.loginout');
let bookingbtn = document.querySelector('.bookingbtn');

let urlapi = "/api/user";

//切換登入；註冊
function useronclick() {

    if (textcontrol) {
        document.querySelector('.inputtextname').hidden = false;
        document.querySelector('.texttop').textContent = "註冊會員帳號";
        document.querySelector('.textend').textContent = "已經有帳戶了？點此登入";
        document.querySelector('.inputbutton').value = "註冊新帳戶";
        document.querySelector(".inputtextname").required = true;
        username = "";
        useremail = "";
        userpassword = "";

    } else {
        document.querySelector('.inputtextname').hidden = true;
        document.querySelector('.texttop').textContent = "登入會員帳號";
        document.querySelector('.textend').textContent = "還沒有帳戶？點此註冊";
        document.querySelector('.inputbutton').value = "登入";
        document.querySelector(".inputtextname").required = false;
        document.querySelector('.textpoint').textContent = ""; //提示狀態
        useremail = "";
        userpassword = "";


    }
    textcontrol = !textcontrol
        // console.log(textcontrol);
}
//登入介面隱藏
function userboxhide() {
    document.querySelector('.userbox').style.display = "none";
    //灰層
    document.getElementById("hidebg").style.display = "none";
}
//登入介面顯示
function userboxshow() {

    document.querySelector('.inputtextname').value = "";
    // document.querySelector('.inputtextemail').value = "";
    // document.querySelector('.inputtextpassword').value = "";
    document.querySelector('.textpoint').textContent = "";
    document.querySelector('.userbox').style.display = "flex";

    //灰層
    let hidebg = document.getElementById("hidebg");
    hidebg.style.display = "block";
    hidebg.style.height = document.body.clientHeight + "px";
}




let form = document.getElementById('signup');
let username = document.querySelector('.inputtextname').value;
let useremail = document.querySelector('.inputtextemail').value;
let userpassword = document.querySelector('.inputtextpassword').value;
form.addEventListener('submit', function(event) {
    let methodtype = " "
    event.preventDefault();
    username == "";
    useremail = "";
    userpassword = "";
    let data = {};
    username = document.querySelector('.inputtextname').value;
    useremail = document.querySelector('.inputtextemail').value;
    userpassword = document.querySelector('.inputtextpassword').value;

    if (username != "") {

        // console.log("註冊")
        data = {
            "name": username,
            "email": useremail,
            "password": userpassword
        }
        methodtype = "POST";
    }
    if (username == "") {
        // console.log("登入")
        data = {
            "email": useremail,
            "password": userpassword
        }
        methodtype = "PATCH";
    }

    fetch(urlapi, {
            method: methodtype,
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(res => {
            return res.json();
        })
        .then(result => {
            // console.log(result);
            if (result.error) {
                document.querySelector('.textpoint').textContent = result.message;
                document.querySelector('.inputtextname').value = "";
            };
            if (result.ok) {
                if (username == "") {
                    // alert("登入成功")
                    logoin();
                    window.location.reload();
                }
                if (username != "") {
                    // alert("註冊成功")
                    textcontrol = !textcontrol
                    window.location.reload();
                }
                userboxhide();
            }
        });




});

function gobooking() {
    location.href = '/booking'
}

function goindex() {
    location.href = '/'
}

//成功 登入 
function logoin() {
    bookingbtn.onclick = gobooking;
    logbtn.onclick = logout;
    logbtn.textContent = "登出";
}

//成功 登出 
function logout() {
    bookingbtn.onclick = userboxshow;

    logbtn.onclick = userboxshow;
    logbtn.textContent = "登入 / 註冊";
    fetch(urlapi, {
        method: 'DELETE'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        // console.log(result);
        if (result.ok) {
            // alert("成功登出")
            window.location.reload();
        }
    })
}


//檢查登入狀況
function checklogstate() {
    fetch(urlapi, {
        method: 'GET'
    }).then(function(res) {
        return res.json();
    }).then(function(result) {
        // console.log(result);

        if (result.data != null) {
            logoin();
        }
        if (document.querySelector('.welcometext')) {
            document.querySelector('.welcometext').textContent = "你好，" + result.data.name + "。";
        }
        if (document.querySelector('.maincenterinput1>input')) {
            document.querySelector('.maincenterinput1>input').value = result.data.name;
        }
        if (document.querySelector('.maincenterinput2>input')) {
            document.querySelector('.maincenterinput2>input').value = result.data.email;
        }

    })
}
checklogstate();