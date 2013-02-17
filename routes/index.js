var crypto =  require('crypto')

exports.index = function(req, res){
	scores = [];
	for (var i=0; i<50; i++){
		var md5sum = crypto.createHash('md5');
		md5sum.update(""+i);
		var rank = (i*4).toString(16);
		while (rank.length < 4)
			rank = "0"+rank;
		scores.push({name:"SimpleGirlfiendVisitor", score:42*(100-i), hash:md5sum.digest('hex'), rank:"0x"+rank})
	}
	res.render("index", {scores:scores});
};
