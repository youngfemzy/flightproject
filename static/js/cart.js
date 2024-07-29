
console.log("hello world")

// get the action buttons which has classname action-btn-clicked 
var action_btn = document.getElementsByClassName('action-btn-clicked')

// loop throught this button to keep checking if it gets clicked --------------------------------------------
for (var i = 0 ; i < action_btn.length ; i++){
    // add an event listener to check for click , on every loop
    action_btn[i].addEventListener('click', function () {
        // if clicked , enter this function
        // now store the data passed from html template file, i.e , in this case product id & action
        // store both in a new variable, to be used 
        var productId = this.dataset.product
        var action = this.dataset.action
        // now we want to do something , with the values we get , as well as action to take

        // just log this out, to check if it is working
        console.log('productId', productId, 'action', action)

        // now we want to do something , with the values we get , as well as action to take



        // TO CHECK IF USER IS AUTHENTICATED , WE FIRST HAVE TO GO TO BASE HTML PAGE, AND get the User Logged IN and 
        // AND STORE RESULT INSIDE var user----- var user = '{{request.user}}'
        // CHECK IF USER IS LOGGED IN OR NOT(AnonymousUser)
       
        if ( user === 'AnonymousUser') {
            console.log(user)
        } 
        else {
            // call function to update user Order & Cart
            updateUserOrder(productId, action);
            
        }
        
    })
}
// END ------- loop throught this button to keep checking if it gets clicked --------------------------------------------





// UPDATE USERS ORDER JS FUNCTION
function updateUserOrder(productId, action) {
    console.log(user, 'Is Logged in , Sending Data....')


    // we set the url that we want to set the post data to , in url.py,   means this is where we want to send the data to
    // then url.py would pass the data we sent to our backend, view.py
    // then we write our query in view.py to work on the data we sent
    var url = '/flight-booking-actions/'
    // var feminame = "femi"
    // console.log('productId', productId, 'action', action , 'feminame', feminame)


    // 1  to use fetch , we first need , the url we want to send the data to
    // 2  the method , i.e what kind of data we are going to send to dat
    fetch(url, {
        method: 'POST',
        // when we are sending post data, we need to pass in some headers with the data
        headers: {
            'Content-Type': 'application/json',
            // CSRF TOKEN FOR PROTECTION IN DJANGO
            'X-CSRFToken': csrftoken,
        },
        
        // after the header, we need to also send a body, the body would contain data we want to send to the backend
        // we also cant send the object datas in raw formart , like this body:{'productId': productId , 'action': action}
        // we need to turn them to string with stingify, like this body:JSON.stringify({'productId': productId , 'action': action})
        body: JSON.stringify({'productId': productId , 'action': action })
        // now that is all we need to do to send this data to the backend , and now our view.py can work on it
    })


    // once we send data to our view.py , we also need to send a promise along with it to the view.py
    // so once view.py recieves & processes our data, if everything goes right , there would be a response throught our promise
    .then((response) =>{
        return response.json()
    })

    // we  turn our response into data, and display response that we go back , from backend view.py
    .then((data) =>{
        console.log('data', data)
        // reload the page , so dat would show
        window.location.reload();
    })
    
}