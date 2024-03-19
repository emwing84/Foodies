document.addEventListener('DOMContentLoaded', function() {

    // Use restaurant button to pull restaurant info
    // document.querySelector("#dropdown-item").addEventListener('click', () => restaurant_info(restaurant.id));

    document.querySelectorAll('select').forEach(item => {
        item.onclick = function(event) {
            const selected = item.value;

            restaurant_info(event, item)
        }
    });

    // Select the post review button to be used later
    const content = document.querySelector('#post-body');
    const post_submit_button = document.querySelector('#post-submit');

    post_submit_button.disabled = true;

    content.onkeyup = () => {
        if (content.value.length > 0 ){
            post_submit_button.disabled = false;
        }
        else {
            post_submit_button.disabled = true;
        }
    }

});

function restaurant_info(event, item) {
    console.log(`id is: ${item.value}`);

    fetch(`/restaurantInfo/${item.value}`)
    .then(response => response.json())
    .then(restaurant => {

        // clear #restaurant-info before appending new info
        document.querySelector('#restaurant-id').innerHTML = "";
        if (document.querySelector('#message')) {
            document.querySelector('#message').innerHTML= "";
        };

        console.log(restaurant)
        const restaurantInfo = document.createElement('div');

        restaurantInfo.innerHTML = `
            <p class="col" > Restaurant location: </p>
            <p class="col" name="address">${restaurant.address}</p>
            <input type="hidden" class="col" name="id" value=${restaurant.id}>
        `;

        document.querySelector('#restaurant-id').append(restaurantInfo);

    });
}