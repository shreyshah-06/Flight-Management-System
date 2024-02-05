var signupForm = document.getElementById("signupForm");
signupForm.addEventListener("submit", submitForm);

async function submitForm(e) {
    e.preventDefault();
    if (!validateForm()) {
        return;
    }
    var formData = new FormData(signupForm);
    let dataObj = Object.fromEntries(formData);
    dataObj['type'] = document.getElementById("type").value;

    let url = `http://127.0.0.1:5000/${dataObj['type']}/signup`;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dataObj)
        });

        console.log(response);

        if (response.status === 200) {
            if (dataObj['type'] === "user") {
                window.location.href = "/dashboard";
            } else {
                window.location.href = "/admindashboard";
            }
        } else if (response.status === 400) {
            console.log("Bad request:", response.statusText);
        } else {
            console.log("Error:", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

function validateForm() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    var emailRegex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,})+$/;
    var passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;

    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return false;
    }
    if (!passwordRegex.test(password)) {
        alert('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number');
        return false;
    }
    return true;
}
