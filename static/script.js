$('button').on('click', function(evt) {
	let word = $(evt.target).previous.val();
	console.log(word);
	axios.get(`http://127.0.0.1:5000/submit?word=${word}`);
});
console.log('heyyyy');
