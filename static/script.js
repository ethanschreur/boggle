let ticking = true;
let total_score = 0;
let used_words = [];

$('button').on('click', async function(evt) {
	// run if time is ticking and when submit button is clicked
	// sends a get request to flask server to see if input is a valid word
	// if it is valid and isn't a repeat, call the change the score function
	if (!ticking) {
		return;
	}
	word = $(evt.target).prev().val();
	response = await axios.get(`http://127.0.0.1:5000/submit?word=${word}`);
	$('p').remove();
	if (used_words.includes(word)) {
		$(evt.target).parent().append('<p>already used word</p>');
	} else {
		$(evt.target).parent().append(`<p>${response.data['result']}</p>`);
		if (response.data['result'] == 'ok') {
			change_score(word);
		}
		used_words.push(word);
	}
});

function change_score(word) {
	// gets the old score from html adds additional score and replaces the score in html
	og_score = parseInt($('span').text());
	new_score = og_score + word.length;
	total_score = new_score;
	$('span').text(new_score.toString());
}

setTimeout(function() {
	// wait a minute, send an alert and sent a post to flask server that sends over the total score
	ticking = false;
	alert("Time's up! Refresh page to begin again.");
	axios.post('http://127.0.0.1:5000/game-over', { score: total_score });
}, 60000);
