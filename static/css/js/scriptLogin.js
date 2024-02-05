var loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", submitFormL);

async function submitFormL(e){
    e.preventDefault();
    var formData = new FormData(loginForm);
    let dataObj = Object.fromEntries(formData);
    dataObj['type'] = (document.getElementById("type").value)
    console.log(dataObj)
    let url = `http://127.0.0.1:5000/${dataObj['type']}/login`
    const response = await fetch(url,{
        method:"POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(dataObj)
    })
    console.log(response)
    if(response.status===200){
        if (dataObj['type'] === "user") {
            window.location.href = "/dashboard";
        } else {
            window.location.href = "/admindashboard";
        }
    }
    else{
        console.log(response)
    }
}