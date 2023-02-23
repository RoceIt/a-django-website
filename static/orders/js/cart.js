// Add item to cart with addtocart class forms
$(document).ready(function(){
    $updatingCartItemCounter = $('#updating_cart_item_counter');
});

$(document).ready(function(){
    $("form.addtocart").submit(function ( event ) {
        event.preventDefault();
        var thisform = $(this).children( "div" );
        var posting = $.post($(this).attr('action'), $(this).serialize(),
                             function( data ) {
                                 thisform.html( data.responseText );
                                 $updatingCartItemCounter.html(
                                     data.itemsInCart);
                             })
            .fail(function( response ) {
                thisform.html(response.responseText);

            })
    }
                              )
});

$(document).ready(function(){
    var $shoppingCartForm = $("#shopping_cart_form")
    $shoppingCartForm.on("change", "input", function(event) {
        if (this.value == 0) {
            console.log('this value is dus 0')
            if (confirm("Are you sure you want to remove this item?") == false) {
                this.value = this.defaultValue;
                return;
            }
        }
        $.post($shoppingCartForm.attr('action'), $(this).serialize(),
                             function( data ) {
                                 $shoppingCartForm.html( data.responseText)
                                 $updatingCartItemCounter.html(
                                     data.itemsInCart);
                             })
            .fail(function( response ) {
                console.log('bad response');

            })
    })
});
