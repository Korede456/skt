
let eye = document.querySelector('.eye')
let password = document.getElementById('phone')


class action {
    toglePassWord(tag) {
        let ClassName = tag.classList.contains('fa-eye-slash')
        if (ClassName == true) {
            tag.classList.replace("fa-eye-slash", "fa-eye")
            password.setAttribute('type', "text")
        } else {
            tag.classList.replace("fa-eye", "fa-eye-slash")
            password.setAttribute('type', "password")
        }
    }
}


let make = new action()
eye.addEventListener('click', function (e) {
    make.toglePassWord(eye)

})