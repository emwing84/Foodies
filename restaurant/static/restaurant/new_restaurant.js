document.addEventListener('DOMContentLoaded', function() {

    // Select the submit button and input to be used later
    const submit = document.querySelector('#submit');
    const name = document.querySelector('#name');
    const address = document.querySelector('#address');

    // Disable submit button by default:
    submit.disabled = true;

    // Listen for input to be typed into the input field
    name.onkeyup = () => {
        if (name.value.length > 0 && address.value.length > 0 ){
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    address.onkeyup = () => {
        if (name.value.length > 0 && address.value.length > 0 ){
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

});