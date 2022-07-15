let messagebox = document.querySelector("#message");
let form = document.getElementById('sentmessage');
// let messageuptext = "";

function previewFile() {
    const preview = document.querySelector('#img');
    const file = document.querySelector('input[type=file]').files[0];
    const reader = new FileReader();
    // console.log("file", file)
    // console.log("reader", reader)

    reader.addEventListener("load", function() {
        // convert image file to base64 string
        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}

form.addEventListener('submit', function(event) {
    event.preventDefault();

    // messageuptext = document.getElementById('sentmessagetext').value;


    // let messages = document.querySelector("messages")

    // if (messagebox.firstChild == null) {
    //     // console.log("無")
    //     messages = document.createElement("div");
    //     messages.className = "messages";
    //     messagebox.appendChild(messages);
    // } else {
    //     // console.log("有")
    //     messages = document.createElement("div");
    //     messages.className = "messages";


    //     messagebox.insertBefore(messages, messagebox.childNodes[0]);
    //     //父.insertBefore(加入，被加入)
    // }
    // messagestext = document.createElement("div");
    // messagestext.className = "messagestext";
    // messagestext.textContent = messageuptext;
    // messages.appendChild(messagestext);

    // messagesimage = document.createElement("img");
    // messagesimage.className = "messagesimage";
    // messages.appendChild(messagesimage);

    // hr = document.createElement("hr");
    // messages.appendChild(hr);


    // const preview = document.querySelector('.messagesimage');
    // const file = document.querySelector('input[type=file]').files[0];
    // const reader = new FileReader();


    // reader.addEventListener("load", function() {
    //     // convert image file to base64 string
    //     preview.src = reader.result;
    // }, false);

    // if (file) {
    //     reader.readAsDataURL(file);
    // }
    let fileField = document.querySelector("input[type='file']");

    if (fileField.files[0] != null) {
        var formData = new FormData();
        formData.append('uptext', document.getElementById('sentmessagetext').value);
        formData.append('upfile', fileField.files[0]);
        // console.log("圖文都有")

    } else {
        var formData = new FormData();
        formData.append('uptext', document.getElementById('sentmessagetext').value);
        // console.log("只有文字")
    }

    fetch("/upindex", {
        method: 'POST',
        body: formData,
        // Other setting you need
        // 不需要設定 'Content-Type': 'multipart/form-data' ，已經用 FormData 物件作為請求內容了
    }).then(function(response) {
        return response.json();
    }).then(function(result) {

        // console.log(result)
        if (result) {
            window.location.reload();
        }
    })

})


function getawsrdsdataapi() {
    fetch("/api/test").then(function(response) {
        return response.json();
    }).then(function(result) {

        // console.log(result)
        // console.log(result.data.length)
        // console.log(result.data[0])

        for (let i = 0; i < result.data.length; i++) {
            if (messagebox.firstChild == null) {
                // console.log("無")
                messages = document.createElement("div");
                messages.className = "messages";
                messagebox.appendChild(messages);
            } else {
                // console.log("有")
                messages = document.createElement("div");
                messages.className = "messages";

                messagebox.insertBefore(messages, messagebox.childNodes[0]);
                //父.insertBefore(加入，被加入)
            }
            messagestext = document.createElement("div");
            messagestext.className = "messagestext";
            messagestext.textContent = result.data[i].text;
            messages.appendChild(messagestext);

            messagesimage = document.createElement("img");
            messagesimage.className = "messagesimage";
            messagesimage.src = result.data[i].imagesrc;
            messages.appendChild(messagesimage);

            hr = document.createElement("hr");
            messages.appendChild(hr);

        }


    })
}

getawsrdsdataapi();