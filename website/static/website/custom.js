	$(".choose-size").on('click',function(){
		$(".choose-size").removeClass('active');
		$(this).addClass('active');

		var _price=$(this).attr('data-price');
		$(".product-price").text(_price);
	})
