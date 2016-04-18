$(document).ready(function(){
	$button=$('#traverseButton');
	$firstView=$('#firstView');
	$title=$('#firstView h1');
	$createdby=$('#firstView p');
	$secondView=$('#secondView');
	$thirdView=$('#thirdView');
	$frontBar=$('#frontBar');
	$leftPanel=$('#leftPanel');
	$topNavBar=$('#navbar');
	$backgroundHome=$('#backgroundhome');

	//created functions for the common practices
	function fadeOpacity(target, enterSpeed, leaveSpeed, untouchedOpacity, touchingOpacity){
		target.mouseenter(function(){
			target.fadeTo(enterSpeed,touchingOpacity);
		})
		target.mouseleave(function(){
			target.fadeTo(leaveSpeed,untouchedOpacity)
		})
	}

	//When user clicks 'TRAVERSE' Button
	$button.click(function(){
		//Making The homepage invisible
		// $firstView.fadeTo('fast', 0)
		$firstView.slideToggle('slow');
		$secondView.fadeTo('slow', 0)
		$thirdView.fadeTo('slow', 0).delay(3000);
		$frontBar.delay(2000).fadeOut().remove();

		//Make second view visible
		$backgroundHome.fadeTo('slow',1);
	});

	//Opacity
	fadeOpacity($topNavBar, 'fast', 'fast', 0.4,0.8);
	fadeOpacity($leftPanel, 'fast', 'fast', 0.3, 0.8);
	fadeOpacity($title,'fast','fast', 1,0.5);
	fadeOpacity($frontBar,'fast', 'fast',1,0.5);
	fadeOpacity($createdby, 'fast','fast',1,0.5);

	

	
	

});
