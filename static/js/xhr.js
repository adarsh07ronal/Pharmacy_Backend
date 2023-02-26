const postBtn = document.getElementById('ci-button');

const sendHttpRequest = (method,url,data) => {
    const promise = new Promise((resolve,reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method,url);
        xhr.setRequestHeader('Content-Type','application/json');
        xhr.onload = () =>{
            if (xhr.status==201){
                resolve(JSON.parse(xhr.response))
            }
            else{
                reject(xhr.response)
            }
        }
        xhr.send(JSON.stringify(data));
    });
    return promise;
}

const sendData = () => {
    sendHttpRequest('POST','https://dev-pharmacy.eoraa.com/api/reset_password/',{
        email : document.querySelector("#email").value,
        password : document.querySelector("#password").value,
        confirm_password : document.querySelector("#conf_password").value,
    })
    .then(responseData => { 
        console.log(responseData)
        document.getElementById("#ci-button").innerHTML = "Success";
        document.getElementById("#form_id").style.visibility = "hidden";
    })
    .catch(err =>{
        console.log(err);
    })
    ;
};

postBtn.addEventListener('click',sendData)