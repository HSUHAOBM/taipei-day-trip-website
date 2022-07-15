let ordernumber = location.href.split("number=");
ordernumber = ordernumber[ordernumber.length - 1]
    // console.log(ordernumber)

function loadorderdataapi() {
    orderapisrc = "/api/orders/" + ordernumber
        // console.log("ordernumberdata", ordernumberdata)
    fetch(orderapisrc).then(function(response) {
        return response.json();
    }).then(function(result) {
        // console.log(result)
        if (result == null) {
            location.href = '/'
        } else {
            addorderdata(result);
            document.getElementById("loadgif").style.display = "none";
        }
    });
}
loadorderdataapi()

function addorderdata(result) {
    // console.log(result.order.trip.attraction.image)
    if (result.order.trip.time == "morning") {
        ordertimetext = "早上 9 點到下午 4 點";
    }
    if (result.order.trip.time == "afternoon") {
        ordertimetext = "下午 2 點到下午 9 點";
    }

    document.querySelector('.order.number').textContent = "訂單編號： " + ordernumber;
    document.querySelector('.order.title').textContent = "導覽行程： 台北－" + result.order.trip.attraction.name + "－導覽一日遊";
    document.querySelector('.order.address').textContent = "導覽地點： " + result.order.trip.attraction.address;

    document.querySelector('.order.time').textContent = "導覽時間： " + result.order.trip.date + "－" + ordertimetext

    document.querySelector('.order.name').textContent = "訂購姓名： " + result.order.contact.name;
    document.querySelector('.order.phone').textContent = "聯絡電話： " + result.order.contact.phone;
    document.querySelector('.order.email').textContent = "聯絡信箱： " + result.order.contact.email;
    document.querySelector('.orderimg>img').src = result.order.trip.attraction.image;
    document.querySelector('.orderimg>img').title = result.order.trip.attraction.name;

}