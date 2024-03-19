document.addEventListener('DOMContentLoaded', function() {

    // run post function when the button is clicked
    document.querySelectorAll('button').forEach(button => {
        button.onclick = function(event) {

            // Check if edit button is clicked
            if (event.target.className === "btn btn-outline-secondary") {
                console.log(`Edit button clicked. Post number: ${this.parentElement.dataset.id}`);

                edit(event, button);

            } else if (event.target.className === "btn btn-outline-danger" || event.target.className === "btn btn-outline-primary") {
                console.log(`Like button clicked. Post number: ${this.parentElement.dataset.id}`);

                // like / unlike a post
                fetch(`/like/${this.parentElement.dataset.id}`, {
                    method:'POST'
                })
                like(event);
            };
        };
    });
});

function edit(event, button) {
    // get post content
    const current_content = event.target.parentElement.querySelector("#post-text").innerHTML;
    console.log(current_content);

    // get innerHTML of edit button
    // const b = event.target.parentElement.querySelector("#edit").innerHTML;

    // get nodeName
    // const c = event.target.parentElement.querySelector("#post-text").nodeName;

    if ((event.target.parentElement.querySelector("#edit").innerHTML) === "Edit") {
        event.target.parentElement.querySelector("#post-text").innerHTML = '<textarea style="width: 48rem" id="edit_text"></textarea>';
        event.target.parentElement.querySelector("#edit_text").value = current_content;
        event.target.parentElement.querySelector("#edit").innerHTML = "Save";

    } else if (event.target.parentElement.querySelector("#edit").innerHTML === "Save") {

        const updated_text = event.target.parentElement.querySelector("#edit_text").value;

        event.target.parentElement.querySelector("#post-text").innerHTML = updated_text;
        event.target.parentElement.querySelector("#edit").innerHTML = "Edit";

        // to update a post
        fetch(`/update/${button.parentElement.dataset.id}`, {
            method: 'POST',
            body: JSON.stringify({
                content: updated_text
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
        });
    };
}

function like(event) {

    // get likes
    var likes = event.target.querySelector("#number").innerHTML;

    // convert to number
    numberOfLikes = Number(likes);
    console.log(numberOfLikes);

    if (event.target.className === "btn btn-outline-danger") {
        event.target.className = "btn btn-outline-primary";
        numberOfLikes--;
        event.target.querySelector("#number").innerHTML = numberOfLikes;

    } else if (event.target.className === "btn btn-outline-primary") {
        event.target.className = "btn btn-outline-danger";
        numberOfLikes++;
        event.target.querySelector("#number").innerHTML = numberOfLikes;
    }
}